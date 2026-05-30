async function runCacheTimingDemo() {
  const chartBox = document.getElementById('timingBars');
  if (!chartBox) return;
  chartBox.innerHTML = ''; // Re-initialize rendering node
  
  const profiles = [
    { label: 'L1 Cache Hit', range: [1, 4], color: 'var(--green)' },
    { label: 'L3 Cache Hit', range: [15, 25], color: 'var(--cyan)' },
    { label: 'Main RAM Miss', range: [90, 135], color: 'var(--red)' }
  ];

  for (const prof of profiles) {
    const value = Math.floor(Math.random() * (prof.range[1] - prof.range[0] + 1)) + prof.range[0];
    const wrapper = document.createElement('div');
    wrapper.className = 'chart-bar-wrapper';
    
    const pct = Math.min((value / 140) * 100, 100);
    
    wrapper.innerHTML = `
      <div class="chart-bar-label">${prof.label}</div>
      <div class="chart-bar-container">
        <div class="chart-bar-fill" style="width: 0%; background: ${prof.color};"></div>
      </div>
    `;
    chartBox.appendChild(wrapper);
    
    setTimeout(() => {
      const fillEl = wrapper.querySelector('.chart-bar-fill');
      if (fillEl) {
        fillEl.style.width = `${pct}%`;
        fillEl.textContent = `${value} ns`;
      }
    }, 40);
  }
}