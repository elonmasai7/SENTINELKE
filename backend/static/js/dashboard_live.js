(function () {
  function parseJsonScript(id, fallback) {
    const node = document.getElementById(id);
    if (!node) {
      return fallback;
    }
    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      console.error('Failed to parse JSON script', id, error);
      return fallback;
    }
  }

  const mapSeed = parseJsonScript('dashboard-map-positions', []);
  const graphNodesSeed = parseJsonScript('dashboard-graph-nodes', []);
  const graphEdgesSeed = parseJsonScript('dashboard-graph-edges', []);
  const alertFeed = document.querySelector('.alert-feed');
  const positionsById = new Map();
  const markersById = new Map();
  const graphState = {
    nodes: graphNodesSeed,
    edges: graphEdgesSeed,
  };
  let map;
  let featureGroup;
  let hasCenteredDemoMap = false;

  const demoRoutes = {
    'demo-1': [
      [-1.28333, 36.81722],
      [-1.28405, 36.81840],
      [-1.28470, 36.81955],
      [-1.28510, 36.82030],
      [-1.28425, 36.81910],
    ],
    'demo-2': [
      [-1.28475, 36.82160],
      [-1.28540, 36.82225],
      [-1.28615, 36.82310],
      [-1.28535, 36.82390],
      [-1.28460, 36.82265],
    ],
    'demo-3': [
      [-1.28690, 36.82440],
      [-1.28755, 36.82330],
      [-1.28810, 36.82220],
      [-1.28730, 36.82145],
      [-1.28655, 36.82285],
    ],
  };

  function severityColor(level) {
    switch ((level || '').toUpperCase()) {
      case 'CRITICAL':
        return '#ff6f6f';
      case 'HIGH':
        return '#ffb14a';
      default:
        return '#7db4ff';
    }
  }

  function markerHtml(position) {
    const level = position.severity || (position.threat_overlay && position.threat_overlay.severity) || 'HIGH';
    const demoTag = position.is_demo ? '<strong>Demo route active</strong>' : '';
    return '<div class="map-badge" style="box-shadow: 0 0 0 0.2rem rgba(0,0,0,0.08); border-color:' + severityColor(level) + '">' +
      '<span>[' + level + '] ' + (position.asset_type || 'asset') + '</span>' +
      '<strong>' + (position.label || position.identifier || 'Unknown') + '</strong>' +
      demoTag +
      '</div>';
  }

  const mapElement = document.getElementById('intelMap');
  if (mapElement && window.L) {
    map = L.map(mapElement, {
      zoomControl: true,
      scrollWheelZoom: false,
      attributionControl: true,
    }).setView([-1.2921, 36.8219], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap',
    }).addTo(map);

    featureGroup = L.featureGroup().addTo(map);
  }

  function normalizePosition(payload) {
    const location = payload.location || {};
    const lat = payload.lat ?? location.lat ?? location.latitude;
    const lng = payload.lng ?? location.lng ?? location.longitude;
    return {
      id: payload.id || payload.identifier,
      asset_type: payload.asset_type || 'asset',
      identifier: payload.identifier || payload.id || 'unknown',
      lat: lat,
      lng: lng,
      label: payload.label || location.label || payload.identifier || 'Unknown',
      severity: payload.severity || (payload.threat_overlay && payload.threat_overlay.severity) || 'HIGH',
      threat_overlay: payload.threat_overlay || {},
      observed_at: payload.observed_at || new Date().toISOString(),
      is_demo: Boolean(payload.is_demo),
    };
  }

  function renderMapPositions(positions, options) {
    if (!map || !featureGroup) {
      return;
    }
    const settings = options || {};
    positions.forEach(function (rawPosition) {
      const position = normalizePosition(rawPosition);
      if (position.lat == null || position.lng == null) {
        return;
      }
      positionsById.set(String(position.id), position);
      const marker = markersById.get(String(position.id));
      if (marker) {
        marker.setLatLng([position.lat, position.lng]);
        marker.setStyle({ color: severityColor(position.severity), fillColor: severityColor(position.severity) });
        marker.setPopupContent(markerHtml(position));
        return;
      }
      const newMarker = L.circleMarker([position.lat, position.lng], {
        radius: position.is_demo ? 10 : 8,
        color: severityColor(position.severity),
        fillColor: severityColor(position.severity),
        fillOpacity: 0.75,
        weight: 2,
      }).bindPopup(markerHtml(position));
      newMarker.addTo(featureGroup);
      markersById.set(String(position.id), newMarker);
    });

    const allPositions = Array.from(positionsById.values());
    if (!allPositions.length) {
      return;
    }
    const demoOnly = allPositions.every(function (position) { return position.is_demo; });
    if (demoOnly && !hasCenteredDemoMap) {
      map.flyTo([-1.2854, 36.8219], 15, { duration: 1.8 });
      hasCenteredDemoMap = true;
      return;
    }
    if (settings.skipFit) {
      return;
    }
    const allMarkers = Array.from(markersById.values());
    if (allMarkers.length === 1) {
      map.setView(allMarkers[0].getLatLng(), 14);
    } else if (allMarkers.length > 1) {
      map.fitBounds(featureGroup.getBounds().pad(demoOnly ? 0.08 : 0.2));
    }
  }

  function updateAlertFeed(position) {
    if (!alertFeed) {
      return;
    }
    const item = document.createElement('div');
    item.className = 'alert-item';
    item.innerHTML =
      '<div class="alert-topline">' +
      '<span class="severity severity-' + (position.severity || 'medium').toLowerCase() + '">[' + (position.severity || 'MEDIUM') + ']</span>' +
      '<span class="alert-location">' + position.label + '</span>' +
      '</div>' +
      '<div class="alert-text">' + position.asset_type + ' update received via live channel</div>';
    alertFeed.prepend(item);
    while (alertFeed.children.length > 6) {
      alertFeed.removeChild(alertFeed.lastElementChild);
    }
  }

  function buildGraphNodesFromPositions() {
    const positionNodes = Array.from(positionsById.values()).slice(0, 5).map(function (position, index) {
      return {
        id: 'live-' + index,
        label: position.label,
        group: (position.severity || 'info').toLowerCase() === 'critical' ? 'danger' : 'info',
        score: position.asset_type,
      };
    });
    const positionEdges = positionNodes.map(function (node) {
      return { source: 'case-nexus', target: node.id, label: 'live' };
    });
    return {
      nodes: graphNodesSeed.concat(positionNodes),
      edges: graphEdgesSeed.concat(positionEdges),
    };
  }

  function renderGraph(graph) {
    const container = document.getElementById('networkGraph');
    if (!container) {
      return;
    }
    const width = container.clientWidth || 520;
    const height = 320;
    const centerX = width / 2;
    const centerY = height / 2;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
    svg.setAttribute('class', 'network-canvas');

    const nodes = graph.nodes || [];
    const edges = graph.edges || [];
    const positioned = new Map();

    nodes.forEach(function (node, index) {
      if (node.id === 'case-nexus') {
        positioned.set(node.id, { x: centerX, y: centerY, radius: 48, node: node });
        return;
      }
      const orbitIndex = index - 1;
      const angle = (Math.PI * 2 * orbitIndex) / Math.max(nodes.length - 1, 1);
      const radius = orbitIndex >= 5 ? 124 : 108;
      positioned.set(node.id, {
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * (orbitIndex >= 5 ? 88 : 118),
        radius: orbitIndex >= 5 ? 26 : 34,
        node: node,
      });
    });

    edges.forEach(function (edge) {
      const source = positioned.get(edge.source);
      const target = positioned.get(edge.target);
      if (!source || !target) {
        return;
      }
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', source.x);
      line.setAttribute('y1', source.y);
      line.setAttribute('x2', target.x);
      line.setAttribute('y2', target.y);
      line.setAttribute('class', 'graph-edge');
      svg.appendChild(line);
    });

    positioned.forEach(function (item) {
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      const group = item.node.group || 'info';
      circle.setAttribute('cx', item.x);
      circle.setAttribute('cy', item.y);
      circle.setAttribute('r', item.radius);
      circle.setAttribute('class', 'graph-node ' + group);
      svg.appendChild(circle);

      const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      label.setAttribute('x', item.x);
      label.setAttribute('y', item.y - 2);
      label.setAttribute('text-anchor', 'middle');
      label.setAttribute('class', 'graph-label');
      label.textContent = item.node.label;
      svg.appendChild(label);

      const score = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      score.setAttribute('x', item.x);
      score.setAttribute('y', item.y + 16);
      score.setAttribute('text-anchor', 'middle');
      score.setAttribute('class', 'graph-score');
      score.textContent = item.node.score;
      svg.appendChild(score);
    });

    container.innerHTML = '';
    container.appendChild(svg);
  }

  function hydrateFromFeed(feed) {
    if (!feed) {
      return;
    }
    if (Array.isArray(feed.map_positions)) {
      renderMapPositions(feed.map_positions);
    }
    if (feed.graph) {
      graphState.nodes = feed.graph.nodes || graphState.nodes;
      graphState.edges = feed.graph.edges || graphState.edges;
      renderGraph(feed.graph);
    } else {
      renderGraph(buildGraphNodesFromPositions());
    }
  }

  function refreshDashboardFeed() {
    fetch('/api/core/dashboard/live-feed/')
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Dashboard feed unavailable');
        }
        return response.json();
      })
      .then(function (payload) {
        hydrateFromFeed(payload);
      })
      .catch(function (error) {
        console.warn(error.message);
      });
  }

  function initSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const socket = new WebSocket(protocol + window.location.host + '/ws/operations/live/');
    socket.onmessage = function (event) {
      try {
        const payload = JSON.parse(event.data);
        if (payload.event === 'bootstrap' && Array.isArray(payload.positions)) {
          renderMapPositions(payload.positions);
          renderGraph(buildGraphNodesFromPositions());
          return;
        }
        if ((payload.event || 'live_position') === 'live_position') {
          const position = normalizePosition(payload);
          renderMapPositions([position]);
          updateAlertFeed(position);
          renderGraph(buildGraphNodesFromPositions());
        }
      } catch (error) {
        console.error('Failed to handle WebSocket payload', error);
      }
    };
    socket.onclose = function () {
      window.setTimeout(initSocket, 3000);
    };
  }

  function animateDemoPositions() {
    const demoPositionIds = Array.from(positionsById.values())
      .filter(function (position) { return position.is_demo && demoRoutes[position.id]; })
      .map(function (position) { return position.id; });
    if (!demoPositionIds.length) {
      return;
    }
    const stepState = {};
    demoPositionIds.forEach(function (id) {
      stepState[id] = 0;
    });
    window.setInterval(function () {
      const updates = demoPositionIds.map(function (id) {
        const route = demoRoutes[id];
        stepState[id] = (stepState[id] + 1) % route.length;
        const point = route[stepState[id]];
        const current = positionsById.get(String(id)) || {};
        return Object.assign({}, current, {
          lat: point[0],
          lng: point[1],
          observed_at: new Date().toISOString(),
          is_demo: true,
        });
      });
      renderMapPositions(updates, { skipFit: true });
      renderGraph(buildGraphNodesFromPositions());
    }, 2600);
  }

  renderMapPositions(mapSeed);
  renderGraph({ nodes: graphNodesSeed, edges: graphEdgesSeed });
  refreshDashboardFeed();
  initSocket();
  window.setTimeout(animateDemoPositions, 1200);
  window.setInterval(refreshDashboardFeed, 30000);
})();
