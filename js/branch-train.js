async function simulateBranchTraining() {
  const logId = 'trainingLogs';
  const confidenceTxt = document.getElementById('predictorConfidence');
  const fillTrack = document.getElementById('confidenceBar');
  
  if (!confidenceTxt || !fillTrack) return;
  
  document.getElementById(logId).innerHTML = '';
  fillTrack.style.width = '0%';
  confidenceTxt.textContent = '0%';
  confidenceTxt.className = 'text-yellow';

  writeLog(logId, 'Allocating boundary training memory blocks...', '#ffffff');
  await sleep(300);

  for (let step = 1; step <= 10; step++) {
    const val = step * 10;
    fillTrack.style.width = `${val}%`;
    confidenceTxt.textContent = `${val}%`;
    
    writeLog(logId, `BTB Loop Cycle [${step}/10]: Valid Pointer address pass -> WITHIN BOUNDS.`);
    await sleep(200);
  }

  confidenceTxt.className = 'text-green';
  writeLog(logId, 'SUCCESS: Branch target predictor conditioned to bypass boundaries speculatively.', 'var(--green)');
}