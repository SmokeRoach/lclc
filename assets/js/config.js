/* =====================================================================
   LOW COST LEGENDS CLUB (LCLC): THE ONE FILE TO EDIT FOR PAYMENTS & MEMBER LINKS
   ---------------------------------------------------------------------
   1. In Whop, create one product per tier (monthly recurring, GBP).
   2. Copy each product's checkout link and paste it between the quotes.
      e.g.  "tier1": "https://whop.com/checkout/plan_XXXXXXXX"
   3. Leave a link as "" and the button shows "checkout opening soon".
   4. Tier 3 stays "coming soon" until tier3Live is true AND a link is set.
   Keep it valid JSON inside the { } (double quotes, no trailing commas).
   After changing prices, run `python3 build.py` so the page text matches
   (the buttons read this file live, so links work without a rebuild).
   ===================================================================== */
window.SAVERS_CONFIG = {
  "provider": "Whop",
  "currency": "£",
  "prices": { "tier1": "4.99", "tier2": "12.99", "tier3": "24.99" },
  "checkout": {
    "tier1": "https://whop.com/checkout/ch_9iEQ6VKnqIyt9QL/",
    "tier2": "https://whop.com/checkout/ch_yXQ9lI0oRYfL69T/",
    "tier3": ""
  },
  "tier3Live": false,
  "memberHub": "https://whop.com/joined/lowcostlegendsclub/",
  "memberLibrary": { "tier1": "https://whop.com/joined/lowcostlegendsclub/exp_M9blLyI3Ck5WDC/app/", "tier2": "https://whop.com/joined/lowcostlegendsclub/exp_3FDW4SE62cJe7d/app/" },
  "manageSubscription": "https://whop.com/@me/settings/orders/",
  "contactEmail": "smokeroach0151@gmail.com",
  "hubUrl": "https://smokeroach.github.io/"
};
