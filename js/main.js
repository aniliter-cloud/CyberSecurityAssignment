// Global Workspace Router Core
function showTab(tabId) {
  // Hide all tab views
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  // Strip active status flags from buttons
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  
  // Activate selection layout blocks
  const targetElement = document.getElementById('tab-' + tabId);
  if (targetElement) {
    targetElement.classList.add('active');
  }
  
  // Set current selected navigation item to active
  if (window.event && window.event.currentTarget) {
    window.event.currentTarget.classList.add('active');
  }
}

// Global Terminal Writer Engine
function writeLog(containerId, text, colorCode = '#58a6ff') {
  const container = document.getElementById(containerId);
  if (!container) return;
  const timestamp = new Date().toLocaleTimeString();
  container.innerHTML += `<div style="color: ${colorCode}; margin-bottom:3px;">[${timestamp}] ${text}</div>`;
  container.scrollTop = container.scrollHeight;
}

const sleep = ms => new Promise(res => setTimeout(res, ms));