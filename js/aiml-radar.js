async function triggerAIMLRadar() {
  const radarLogId = 'aimlLogs';
  const complianceOutput = document.getElementById('aimlVerdict');
  if (!complianceOutput) return;

  document.getElementById(radarLogId).innerHTML = '';
  complianceOutput.textContent = 'ANALYZING TELEMETRY';
  complianceOutput.className = 'verdict-output text-yellow';

  const nodes = {
    branch: document.getElementById('sigBranch'),
    l1: document.getElementById('sigL1'),
    stride: document.getElementById('sigStride'),
    time: document.getElementById('sigTime')
  };

  const updateNodeStyles = (b, l, s, t) => {
    nodes.branch.className = b === 'Normal' ? 'text-green' : 'text-red'; nodes.branch.textContent = b;
    nodes.l1.className = l === 'Normal' ? 'text-green' : 'text-red'; nodes.l1.textContent = l;
    nodes.stride.className = s === 'Normal' ? 'text-green' : 'text-red'; nodes.stride.textContent = s;
    nodes.time.className = t === 'Normal' ? 'text-green' : 'text-red'; nodes.time.textContent = t;
  };

  writeLog(radarLogId, 'Opening telemetry channel connections to Hardware Counter registers...', '#ffffff');
  updateNodeStyles('Normal', 'Normal', 'Normal', 'Normal');
  await sleep(600);

  writeLog(radarLogId, 'LSTM Context Evaluation: Tracking baseline thread runtime loops...');
  await sleep(600);

  writeLog(radarLogId, 'WARNING: BTB branch target buffer misprediction spike observed.', 'var(--yellow)');
  updateNodeStyles('MISPREDICT HIGH', 'Normal', 'Normal', 'Normal');
  await sleep(600);

  writeLog(radarLogId, 'ALERT: Cache flushing behavior confirmed via iterative line evictions.', 'var(--yellow)');
  updateNodeStyles('MISPREDICT HIGH', 'BURST EVICT', 'Normal', 'Normal');
  await sleep(600);

  writeLog(radarLogId, 'CRITICAL: Linear 512-byte element stride array scanning pattern detected!', 'var(--red)');
  updateNodeStyles('MISPREDICT HIGH', 'BURST EVICT', 'STRIDE FOUND', 'ASYMMETRY DELTA');
  await sleep(500);

  writeLog(radarLogId, 'VERDICT: Spectre Variant 1 pattern matched with 98.4% model confidence.', 'var(--cyan)');
  complianceOutput.textContent = '🚨 ATTACK THWARTED BY LSTM GUARD ENGINE';
  complianceOutput.className = 'verdict-output text-red';
}