(function () {
  function getCsrfToken() {
    const cookieMatch = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    if (cookieMatch) {
      return cookieMatch.pop();
    }
    const hiddenToken = document.querySelector('#globalCsrfForm input[name="csrfmiddlewaretoken"]');
    return hiddenToken ? hiddenToken.value : '';
  }

  function showAlert(message, level) {
    const host = document.getElementById('actionFeedback');
    if (!host) {
      return;
    }
    const alert = document.createElement('div');
    alert.className = 'alert alert-' + (level || 'info') + ' border-0 shadow-sm command-alert';
    alert.textContent = message;
    host.prepend(alert);
    window.setTimeout(function () {
      alert.remove();
    }, 5000);
  }

  function setButtonLoading(button, loading) {
    if (!button) {
      return;
    }
    if (loading) {
      button.dataset.originalText = button.innerHTML;
      button.disabled = true;
      button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading';
    } else {
      button.disabled = false;
      button.innerHTML = button.dataset.originalText || button.innerHTML;
    }
  }

  const searchForm = document.getElementById('dashboardSearchForm');
  const searchInput = document.getElementById('dashboardSearchInput');
  const searchRoutes = [
    { terms: ['case', 'cases'], url: '/cases/' },
    { terms: ['incident', 'incidents'], url: '/incidents/' },
    { terms: ['dispatch', 'officer', 'officers'], url: '/dispatch/' },
    { terms: ['field', 'ops'], url: '/field-ops/' },
    { terms: ['watchlist', 'suspect'], url: '/watchlist/' },
    { terms: ['wallet', 'wallets', 'crypto'], url: '/crypto-tracing/' },
    { terms: ['network', 'graph', 'device', 'devices'], url: '/network-graph/' },
    { terms: ['ai', 'brief', 'voice', 'analysis'], url: '/ai-assistant/' },
    { terms: ['health', 'audit', 'compliance', 'warrant'], url: '/system-health/' }
  ];

  if (searchForm && searchInput) {
    searchForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const query = searchInput.value.trim().toLowerCase();
      const match = searchRoutes.find(function (entry) {
        return entry.terms.some(function (term) {
          return query.indexOf(term) !== -1;
        });
      });
      window.location.href = match ? match.url : '/';
    });
  }

  document.querySelectorAll('form.inline-action-form, form.modal-form').forEach(function (form) {
    form.addEventListener('submit', function () {
      setButtonLoading(form.querySelector('button[type="submit"]'), true);
    });
  });

  function aiPayload(action) {
    const caseId = document.getElementById('aiCaseId');
    const sensitivity = document.getElementById('aiSensitivity');
    const reportText = document.getElementById('aiReportText');
    const entityId = document.getElementById('aiEntityId');
    const voiceQuery = document.getElementById('aiVoiceQuery');
    const payloads = {
      summary: { report_text: reportText ? reportText.value : '', sensitivity_level: sensitivity ? sensitivity.value : 'restricted' },
      threat: { entity_id: entityId ? entityId.value : 'entity-case-nexus', sensitivity_level: sensitivity ? sensitivity.value : 'restricted' },
      brief: { case_id: caseId && caseId.value ? Number(caseId.value) : null, sensitivity_level: sensitivity ? sensitivity.value : 'restricted' },
      voice: { query: voiceQuery ? voiceQuery.value : '', sensitivity_level: sensitivity ? sensitivity.value : 'restricted' }
    };
    const payload = payloads[action] || {};
    if (caseId && caseId.value && action !== 'brief') {
      payload.case_id = Number(caseId.value);
    }
    Object.keys(payload).forEach(function (key) {
      if (payload[key] === null || payload[key] === '') {
        delete payload[key];
      }
    });
    return payload;
  }

  const aiOutput = document.getElementById('aiActionOutput');
  const aiStatusBanner = document.getElementById('aiStatusBanner');
  document.querySelectorAll('.ai-service-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      const endpoint = button.getAttribute('data-ai-endpoint');
      const action = button.getAttribute('data-ai-action');
      const payload = aiPayload(action);
      setButtonLoading(button, true);
      if (aiStatusBanner) {
        aiStatusBanner.textContent = 'Running request...';
        aiStatusBanner.className = 'service-status-banner';
      }
      fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(payload)
      })
        .then(function (response) {
          return response.json().catch(function () { return { detail: 'Tool temporarily unavailable' }; }).then(function (data) {
            if (!response.ok) {
              throw new Error(data.detail || data.message || 'Tool temporarily unavailable');
            }
            return data;
          });
        })
        .then(function (data) {
          if (aiStatusBanner) {
            aiStatusBanner.textContent = 'Request completed successfully.';
            aiStatusBanner.className = 'service-status-banner success';
          }
          if (aiOutput) {
            aiOutput.textContent = JSON.stringify(data, null, 2);
          }
          showAlert('AI action completed successfully.', 'success');
        })
        .catch(function (error) {
          if (aiStatusBanner) {
            aiStatusBanner.textContent = error.message + ' Retry or view logs.';
            aiStatusBanner.className = 'service-status-banner error';
          }
          if (aiOutput) {
            aiOutput.textContent = JSON.stringify({ error: error.message, logs: '/audit-logs/' }, null, 2);
          }
          showAlert(error.message, 'danger');
        })
        .finally(function () {
          setButtonLoading(button, false);
        });
    });
  });

  document.querySelectorAll('.tool-service-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      const endpoint = button.getAttribute('data-tool-endpoint');
      const statusBanner = button.closest('.intel-card').querySelector('.service-status-banner');
      setButtonLoading(button, true);
      if (statusBanner) {
        statusBanner.textContent = 'Running action...';
        statusBanner.className = 'service-status-banner';
      }
      fetch(endpoint, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken()
        }
      })
        .then(function (response) {
          return response.json().then(function (data) {
            if (!response.ok || data.ok === false) {
              throw new Error(data.message || 'Tool temporarily unavailable');
            }
            return data;
          });
        })
        .then(function (data) {
          if (statusBanner) {
            statusBanner.textContent = data.message;
            statusBanner.className = 'service-status-banner success';
          }
          showAlert(data.message, 'success');
          if (data.redirect_url) {
            window.setTimeout(function () {
              window.location.href = data.redirect_url;
            }, 500);
          }
        })
        .catch(function (error) {
          if (statusBanner) {
            statusBanner.textContent = error.message + ' Retry or view logs.';
            statusBanner.className = 'service-status-banner error';
          }
          showAlert(error.message, 'danger');
        })
        .finally(function () {
          setButtonLoading(button, false);
        });
    });
  });
})();
