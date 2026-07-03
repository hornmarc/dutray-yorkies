async function loadPuppies() {
  const target = document.querySelector('[data-puppies]');
  if (!target) return;
  try {
    const res = await fetch('/data/puppies.json');
    const puppies = await res.json();
    target.innerHTML = puppies.map(puppy => `
      <article class="card puppy-card">
        <img src="${puppy.photo || '/images/uploads/placeholder-puppy.jpg'}" alt="${puppy.name} the Yorkie puppy">
        <p><span class="status ${puppy.status.toLowerCase() === 'sold' ? 'sold' : ''}">${puppy.status}</span></p>
        <h3>${puppy.name}</h3>
        <p><strong>${puppy.gender}</strong>${puppy.birthdate ? ` • Born ${puppy.birthdate}` : ''}</p>
        <p>${puppy.description}</p>
      </article>
    `).join('');
  } catch (err) {
    target.innerHTML = '<p>Puppy listings are being updated. Please check back soon.</p>';
  }
}
loadPuppies();
