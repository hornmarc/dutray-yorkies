// Holiday Banner
async function loadHolidayBanner() {
  try {
    const res = await fetch('/data/holiday.json');
    const holiday = await res.json();
    if (!holiday.active) return;

    const banner = document.createElement('div');
    banner.className = 'holiday-banner';
    banner.style.background = holiday.colors.background;
    banner.style.color = holiday.colors.text;
    banner.innerHTML = `<div class="container">${holiday.emoji} ${holiday.message} ${holiday.emoji}</div>`;

    // Add floating particles
    const particles = document.createElement('div');
    particles.className = 'holiday-particles';
    const particleEmojis = holiday.particles || [holiday.emoji];
    for (let i = 0; i < 12; i++) {
      const span = document.createElement('span');
      span.textContent = particleEmojis[i % particleEmojis.length];
      span.style.left = Math.random() * 100 + '%';
      span.style.animationDelay = (Math.random() * 4) + 's';
      span.style.animationDuration = (3 + Math.random() * 3) + 's';
      particles.appendChild(span);
    }
    banner.appendChild(particles);

    const header = document.querySelector('.site-header');
    header.insertAdjacentElement('afterend', banner);
  } catch (err) {
    // No holiday banner — that's fine
  }
}

// Load Puppies
async function loadPuppies() {
  const target = document.querySelector('[data-puppies]');
  if (!target) return;
  try {
    const res = await fetch('/data/puppies.json');
    const puppies = await res.json();
    target.innerHTML = puppies.map(puppy => `
      <article class="card puppy-card">
        <img src="${puppy.photo || '/images/uploads/placeholder-puppy.jpg'}" alt="${puppy.name} the Yorkie puppy">
        ${renderVideo(puppy)}
        <p><span class="status ${puppy.status.toLowerCase() === 'sold' ? 'sold' : ''}">${puppy.status}</span></p>
        <h3>${puppy.name}</h3>
        <p><strong>${puppy.gender}</strong>${puppy.birthdate ? ` &bull; Born ${puppy.birthdate}` : ''}</p>
        <p>${puppy.description}</p>
      </article>
    `).join('');
  } catch (err) {
    target.innerHTML = '<p>Puppy listings are being updated. Please check back soon.</p>';
  }
}

/**
 * Render video embed or self-hosted video for a puppy.
 * Supports YouTube, Facebook, and direct .mp4 file paths.
 */
function renderVideo(puppy) {
  const url = puppy.video || '';
  const file = puppy.videoFile || '';

  // YouTube embed
  const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]+)/);
  if (ytMatch) {
    return `<div class="video-embed"><iframe src="https://www.youtube.com/embed/${ytMatch[1]}" frameborder="0" allowfullscreen loading="lazy" title="Video of ${puppy.name}"></iframe></div>`;
  }

  // Facebook video embed
  if (url.includes('facebook.com') || url.includes('fb.watch')) {
    const encoded = encodeURIComponent(url);
    return `<div class="video-embed"><iframe src="https://www.facebook.com/plugins/video.php?href=${encoded}&show_text=false" frameborder="0" allowfullscreen loading="lazy" title="Video of ${puppy.name}"></iframe></div>`;
  }

  // Generic video URL (Vimeo, etc.) — link with play button overlay
  if (url) {
    return `<a class="video-link" href="${url}" target="_blank" rel="noopener" aria-label="Watch video of ${puppy.name}"><span class="play-icon">&#9654;</span> Watch Video</a>`;
  }

  // Self-hosted mp4
  if (file) {
    return `<div class="video-embed"><video controls preload="metadata" poster="${puppy.photo || ''}"><source src="${file}" type="video/mp4">Your browser does not support video.</video></div>`;
  }

  return '';
}

// Load Testimonials
async function loadTestimonials() {
  const target = document.querySelector('[data-testimonials]');
  if (!target) return;
  try {
    const res = await fetch('/data/testimonials.json');
    const testimonials = await res.json();
    target.innerHTML = testimonials.map(t => `
      <article class="card testimonial-card">
        ${t.photo ? `<img src="${t.photo}" alt="Photo from ${t.name}">` : ''}
        <blockquote>${t.text}</blockquote>
        <p class="testimonial-author">&mdash; ${t.name}</p>
      </article>
    `).join('');
  } catch (err) {
    target.innerHTML = '<p>Testimonials are being updated. Please check back soon.</p>';
  }
}

// Load Dams + Sires
async function loadDamsSires() {
  const damsTarget = document.querySelector('[data-dams]');
  const siresTarget = document.querySelector('[data-sires]');
  if (!damsTarget && !siresTarget) return;
  try {
    const res = await fetch('/data/dams-sires.json');
    const data = await res.json();

    if (damsTarget) {
      damsTarget.innerHTML = data.dams.map(dog => `
        <article class="card dog-card">
          <img src="${dog.photo}" alt="${dog.name} - ${dog.color} Yorkie dam">
          <h3>${dog.name}</h3>
          <ul class="dog-details">
            <li><strong>Color:</strong> ${dog.color}</li>
            <li><strong>Weight:</strong> ${dog.weight}</li>
            <li><strong>Registration:</strong> ${dog.registration}</li>
          </ul>
          ${dog.description ? `<p>${dog.description}</p>` : ''}
        </article>
      `).join('');
    }

    if (siresTarget) {
      siresTarget.innerHTML = data.sires.map(dog => `
        <article class="card dog-card">
          <img src="${dog.photo}" alt="${dog.name} - ${dog.color} Yorkie sire">
          <h3>${dog.name}</h3>
          <ul class="dog-details">
            <li><strong>Color:</strong> ${dog.color}</li>
            <li><strong>Weight:</strong> ${dog.weight}</li>
            <li><strong>Registration:</strong> ${dog.registration}</li>
          </ul>
          ${dog.description ? `<p>${dog.description}</p>` : ''}
        </article>
      `).join('');
    }
  } catch (err) {
    if (damsTarget) damsTarget.innerHTML = '<p>Content is being updated. Please check back soon.</p>';
    if (siresTarget) siresTarget.innerHTML = '';
  }
}

// Mobile menu toggle
function initMobileMenu() {
  const header = document.querySelector('.header-inner');
  const nav = document.querySelector('.nav');
  if (!header || !nav) return;

  // Create hamburger button
  const toggle = document.createElement('button');
  toggle.className = 'menu-toggle';
  toggle.setAttribute('aria-label', 'Toggle navigation menu');
  toggle.innerHTML = '<span></span>';
  header.appendChild(toggle);

  toggle.addEventListener('click', () => {
    nav.classList.toggle('open');
    toggle.classList.toggle('open');
  });

  // Close menu when a link is clicked
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.classList.remove('open');
    });
  });
}

// Initialize
initMobileMenu();
loadHolidayBanner();
loadPuppies();
loadTestimonials();
loadDamsSires();
