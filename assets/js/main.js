/* Low Cost Legends Club (LCLC) by SmokeRoach: wires buttons to assets/js/config.js. No tracking, no cookies. */
(function(){
  var C = window.SAVERS_CONFIG || {checkout:{},memberLibrary:{},prices:{}};
  var names = {tier1:"Tier 1", tier2:"Tier 2", tier3:"Tier 3"};
  var toast;
  function say(msg){
    if(!toast){toast=document.createElement("div");toast.className="toast";toast.setAttribute("role","status");document.body.appendChild(toast);}
    toast.textContent=msg;toast.classList.add("show");clearTimeout(say.t);say.t=setTimeout(function(){toast.classList.remove("show")},4200);
  }
  function ok(u){return typeof u==="string" && /^https:\/\//.test(u);}

  // Live prices
  document.querySelectorAll("[data-price]").forEach(function(el){
    var p=C.prices&&C.prices[el.dataset.price]; if(p) el.textContent=(C.currency||"£")+p;
  });

  // Subscribe buttons
  document.querySelectorAll("[data-checkout]").forEach(function(btn){
    var tier=btn.dataset.checkout, url=C.checkout&&C.checkout[tier];
    var note=btn.parentNode.querySelector(".btn-note");
    if(tier==="tier3" && !C.tier3Live){ return; } // waitlist button keeps its mailto
    if(ok(url)){
      btn.href=url; btn.target="_blank"; btn.rel="noopener";
      if(note) note.textContent="Secure checkout by "+(C.provider||"Whop")+". Cancel any time.";
    } else {
      btn.setAttribute("aria-disabled","true");
      if(note) note.textContent="Checkout opening soon. Join the free guides in the meantime.";
      btn.addEventListener("click",function(e){e.preventDefault();say(names[tier]+" checkout is opening very soon. The free guides are open to everyone right now.");});
    }
  });

  // Member links (read the full guide on Whop)
  document.querySelectorAll("[data-member]").forEach(function(a){
    var key=a.dataset.member, url=key==="hub"?C.memberHub:(C.memberLibrary&&C.memberLibrary[key])||C.memberHub;
    if(key==="manage") url=C.manageSubscription;
    if(ok(url)){a.href=url;a.target="_blank";a.rel="noopener";}
    else{a.addEventListener("click",function(e){e.preventDefault();say("The members' area opens when subscriptions go live.");});}
  });

  // Mobile menu
  var mb=document.querySelector(".menu-btn"), mn=document.getElementById("mnav");
  if(mb&&mn){mb.addEventListener("click",function(){var o=mn.classList.toggle("open");mb.setAttribute("aria-expanded",o);mb.textContent=o?"✕":"☰";});}
})();
