
/* The paid-funnel treatment redirects to app.arcads.ai, and its impression is
   held back until that page loads. Across hostnames the default carrier is a
   root-domain cookie that lives one minute — Safari's storage rules and a slow
   landing both lose it, and the arm reads as smaller than it is. The URL
   carrier survives both. Must sit above the tag that reads it. */
window.experimentConfig = {
  redirectConfig: { encodeRedirectInCookie: true, encodeRedirectInUrl: true },
};
