
document.addEventListener("click", function (e) {
  const button = e.target.closest(".button");
  if (!button) return;
  const ampDeviceId = localStorage.getItem("ampl_dev_id");
  if (!ampDeviceId) return;
  const href = button.getAttribute("href");
  if (!href || href.includes("ampl_dev_id=")) return;
  e.preventDefault();
  const separator = href.includes("?") ? "&" : "?";
  const newUrl =
    href + separator + "ampl_dev_id=" + encodeURIComponent(ampDeviceId);
  window.location.href = newUrl;
});
