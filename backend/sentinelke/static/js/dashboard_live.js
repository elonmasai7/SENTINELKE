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
    return '<div class="map-badge" style="box-shadow: 0 0 0 0.2rem rgba(0,0,0,0.08); border-color:' + severityColor(level) + '">' +
      '<span>[' + level + '] ' + (position.asset_type || 'asset') + '</span>' +
      '<strong>' + (position.label || position.identifier || 'Unknown') + '</strong>' +
      '</div>';
  }

  const mapElement = document.getElementById('intelMap');
  let map;
  let featureGroup;
  if (mapElement && window.L) {
    map = L.map(mapElement, {
      zoomControl: true,
      scrollWheelZoom: false,
      attributionControl: true,
    }).setView([-1.2921, 36.8219], 6);

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
    };
  }

  function renderMapPositions(positions) {
    if (!map || !featureGroup) {
      return;
    }
    positions.forEach(function (rawPosition) {
      const position = normalizePosition(rawPosition);
      if (position.lat == null || position.lng == null) {
        return;
      }
      positionsById.set(String(position.id), position);
      const marker = markersById.get(String(position.id));
      if (marker) {
        marker.setLatLng([position.lat, position.lng]);
        marker.setPopupContent(markerHtml(position));
        return;
      }
      const newMarker = L.circleMarker([position.lat, position.lng], {
        radius: 8,
        color: severityColor(position.severity),
        fillColor: severityColor(position.severity),
        fillOpacity: 0.75,
        weight: 2,
      }).bindPopup(markerHtml(position));
      newMarker.addTo(featureGroup);
      markersById.set(String(position.id), newMarker);
    });

    const allMarkers = Array.from(markersById.values());
    if (allMarkers.length === 1) {
      map.setView(allMarkers[0].getLatLng(), 10);
    } else if (allMarkers.length > 1) {
      map.fitBounds(featureGroup.getBounds().pad(0.2));
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

  renderMapPositions(mapSeed);
  renderGraph({ nodes: graphNodesSeed, edges: graphEdgesSeed });
  refreshDashboardFeed();
  initSocket();
  window.setInterval(refreshDashboardFeed, 30000);
})();
