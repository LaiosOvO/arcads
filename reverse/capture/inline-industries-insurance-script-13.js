
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }

  // Quand la page est complètement chargée
  window.addEventListener('load', () => {
    // Petit délai pour éviter que le navigateur remette le scroll après coup
    setTimeout(() => {
      window.scrollTo(0, 0);
    }, 50);
  });
