function initMatrixDisplay() {
  const grid = document.getElementById('probeMatrix');
  if (!grid) return;
  grid.innerHTML = '';
  
  for (let i = 0; i < 256; i++) {
    const cell = document.createElement('div');
    cell.className = 'matrix-cell cold';
    cell.id = `cell-${i}`;
    cell.textContent = i.toString(16).toUpperCase().padStart(2, '0');
    grid.appendChild(cell);
  }
}

async function executeProbeScan(customValue = null, silently = false) {
  const grid = document.getElementById('probeMatrix');
  if (!grid || !grid.children.length) initMatrixDisplay();

  const selection = customValue || document.getElementById('targetSecret').value;
  const envNoise = document.getElementById('noiseLevel').value;
  const targetCode = selection.charCodeAt(0);

  // Clear existing cell heat mappings
  document.querySelectorAll('.matrix-cell').forEach(c => c.className = 'matrix-cell cold');

  let jitterPct = envNoise === 'low' ? 10 : (envNoise === 'high' ? 38 : 0);

  for (let i = 0; i < 256; i++) {
    let latency = Math.floor(Math.random() * 40) + 85;
    
    if (i === targetCode) {
      latency = Math.floor(Math.random() * 8) + 5; // Simulates quick cache lines
    } else if (jitterPct > 0 && Math.random() * 100 < jitterPct) {
      latency = Math.floor(Math.random() * 35) + 30; // Simulates pipeline noise anomalies
    }

    const cellElement = document.getElementById(`cell-${i}`);
    if (cellElement) {
      if (latency < 30) cellElement.className = 'matrix-cell hot';
      else if (latency < 80) cellElement.className = 'matrix-cell warm';
    }
  }

  if (!silently) {
    document.getElementById('leakOutput').textContent = `[ ${String.fromCharCode(targetCode)} ]`;
  }
  return String.fromCharCode(targetCode);
}

async function executeFullAttack() {
  const attackVector = "SPECTRE";
  const outputEl = document.getElementById('leakOutput');
  outputEl.textContent = "";
  let buffer = "";

  for (let char of attackVector) {
    const charOut = await executeProbeScan(char, true);
    buffer += charOut;
    outputEl.textContent = buffer;
    await sleep(500);
  }
}

// Bind matrix constructor to engine mounts
document.addEventListener("DOMContentLoaded", initMatrixDisplay);