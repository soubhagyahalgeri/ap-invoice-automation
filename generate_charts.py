<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>AP Invoice Automation — Control Tower</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.4/chart.umd.min.js"></script>
<style>
  :root{
    --bg-deep:#14181D; --bg-paper:#ECEEE8; --surface:#FFFFFF; --ink:#1F2630;
    --ink-soft:#5B6471; --accent-teal:#1F6F78; --accent-teal-soft:#E3EFEF;
    --accent-amber:#B8853A; --accent-amber-soft:#F6ECDC; --accent-rust:#A84432;
    --accent-rust-soft:#F4E3DE; --accent-moss:#4F7A56; --accent-moss-soft:#E6EFE5;
    --line:#D7D9D0; --line-deep:#2B323C;
  }
  *{box-sizing:border-box;}
  body{margin:0;font-family:'Inter',sans-serif;background:var(--bg-paper);color:var(--ink);}
  .mono{font-family:'IBM Plex Mono',monospace;}
  .app{display:grid;grid-template-columns:240px 1fr;min-height:100vh;}
  /* Sidebar */
  .sidebar{background:var(--bg-deep);color:#fff;padding:22px 18px;display:flex;flex-direction:column;gap:22px;}
  .brand{font-weight:800;font-size:15px;letter-spacing:.02em;}
  .brand small{display:block;font-weight:500;color:#8B96A3;font-size:11px;margin-top:3px;letter-spacing:.04em;text-transform:uppercase;}
  .nav{display:flex;flex-direction:column;gap:3px;margin-top:4px;}
  .nav button{all:unset;cursor:pointer;padding:9px 10px;border-radius:7px;font-size:13.5px;font-weight:500;color:#C3CAD2;display:flex;justify-content:space-between;align-items:center;}
  .nav button:hover{background:#1C2229;color:#fff;}
  .nav button.active{background:var(--accent-teal);color:#fff;}
  .nav button .count{font-family:'IBM Plex Mono',monospace;font-size:11px;background:rgba(255,255,255,.14);padding:1px 6px;border-radius:10px;}
  .side-kpis{margin-top:auto;border-top:1px solid #262D36;padding-top:16px;display:flex;flex-direction:column;gap:10px;}
  .side-kpi-label{font-size:10.5px;color:#7E8995;text-transform:uppercase;letter-spacing:.06em;}
  .side-kpi-val{font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;}
  /* Main */
  main{padding:22px 26px 40px;overflow-x:hidden;}
  .topbar{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:18px;flex-wrap:wrap;}
  .topbar h1{font-size:19px;margin:0 0 4px;font-weight:700;}
  .topbar p{margin:0;color:var(--ink-soft);font-size:13px;max-width:560px;}
  .actions{display:flex;gap:8px;flex-wrap:wrap;}
  button.btn{all:unset;cursor:pointer;font-family:'Inter',sans-serif;font-weight:600;font-size:12.5px;padding:9px 14px;border-radius:7px;border:1px solid var(--line);background:var(--surface);color:var(--ink);transition:.15s;}
  button.btn:hover{border-color:var(--accent-teal);color:var(--accent-teal);}
  button.btn.primary{background:var(--accent-teal);color:#fff;border-color:var(--accent-teal);}
  button.btn.primary:hover{background:#185a61;color:#fff;}
  button.btn:disabled{opacity:.45;cursor:not-allowed;}
  button.btn.small{padding:5px 10px;font-size:11.5px;}
  /* Pipeline rail (signature element) */
  .rail{display:flex;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 26px;margin-bottom:18px;overflow-x:auto;}
  .rail-node{display:flex;flex-direction:column;align-items:center;min-width:108px;position:relative;}
  .rail-dot{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:14px;border:2px solid var(--line);background:var(--bg-paper);color:var(--ink-soft);transition:.25s;}
  .rail-node.active .rail-dot{transform:scale(1.12);}
  .rail-label{font-size:11px;margin-top:7px;color:var(--ink-soft);font-weight:600;text-align:center;text-transform:uppercase;letter-spacing:.03em;}
  .rail-line{flex:1;height:2px;background:var(--line);margin:0 2px;position:relative;top:-12px;min-width:24px;}
  .st-queued .rail-dot{border-color:#9AA3AE;color:#6B7480;}
  .st-processing .rail-dot{border-color:var(--accent-teal);color:var(--accent-teal);background:var(--accent-teal-soft);animation:pulse 1.1s infinite;}
  .st-exception .rail-dot{border-color:var(--accent-rust);color:var(--accent-rust);background:var(--accent-rust-soft);}
  .st-pending .rail-dot{border-color:var(--accent-amber);color:var(--accent-amber);background:var(--accent-amber-soft);}
  .st-posted .rail-dot{border-color:var(--accent-moss);color:var(--accent-moss);background:var(--accent-moss-soft);}
  @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(31,111,120,.35);}70%{box-shadow:0 0 0 8px rgba(31,111,120,0);}100%{box-shadow:0 0 0 0 rgba(31,111,120,0);}}
  /* Tabs */
  .tab{display:none;}
  .tab.active{display:block;}
  .grid-kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:18px;}
  .kpi-card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px 16px;}
  .kpi-card .label{font-size:11px;color:var(--ink-soft);text-transform:uppercase;letter-spacing:.04em;font-weight:600;}
  .kpi-card .val{font-family:'IBM Plex Mono',monospace;font-size:25px;font-weight:700;margin-top:5px;}
  .kpi-card .sub{font-size:11px;color:var(--ink-soft);margin-top:3px;}
  .charts-row{display:grid;grid-template-columns:1.1fr 1fr;gap:14px;margin-bottom:18px;}
  .panel{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;}
  .panel h3{margin:0 0 12px;font-size:13.5px;font-weight:700;}
  table{width:100%;border-collapse:collapse;font-size:12.5px;}
  th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink-soft);padding:8px 10px;border-bottom:1px solid var(--line);}
  td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:middle;}
  tr.clickable{cursor:pointer;}
  tr.clickable:hover{background:var(--bg-paper);}
  .pill{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;padding:3px 9px;border-radius:20px;}
  .pill-queued{background:#EDEFEA;color:#6B7480;}
  .pill-processing{background:var(--accent-teal-soft);color:var(--accent-teal);}
  .pill-exception{background:var(--accent-rust-soft);color:var(--accent-rust);}
  .pill-pending_approval{background:var(--accent-amber-soft);color:var(--accent-amber);}
  .pill-posted{background:var(--accent-moss-soft);color:var(--accent-moss);}
  .empty{color:var(--ink-soft);font-size:12.5px;padding:30px 10px;text-align:center;}
  /* Modal */
  .modal-overlay{position:fixed;inset:0;background:rgba(20,24,29,.55);display:flex;align-items:center;justify-content:center;padding:24px;z-index:50;}
  .modal-overlay.hidden{display:none;}
  .modal{background:var(--surface);border-radius:14px;max-width:980px;width:100%;max-height:88vh;overflow-y:auto;padding:22px 26px;}
  .modal-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;}
  .modal-head h2{margin:0;font-size:16px;}
  .modal-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
  .modal-grid img{width:100%;border:1px solid var(--line);border-radius:8px;}
  .kv{display:grid;grid-template-columns:120px 1fr;gap:4px 10px;font-size:12.5px;margin-bottom:3px;}
  .kv b{color:var(--ink-soft);font-weight:600;}
  .diff-ok{color:var(--accent-moss);}
  .diff-bad{color:var(--accent-rust);font-weight:700;}
  .issue-row{background:var(--accent-rust-soft);border-radius:6px;padding:7px 10px;font-size:12px;margin-bottom:5px;}
  .close-x{all:unset;cursor:pointer;font-size:18px;color:var(--ink-soft);}
  .info-banner{background:var(--accent-teal-soft);color:#13474D;border-radius:8px;padding:10px 14px;font-size:12px;margin-bottom:16px;line-height:1.5;}
  .log-row{font-size:12px;padding:6px 0;border-bottom:1px solid var(--line);}
  .log-time{color:var(--ink-soft);margin-right:8px;}
  .scenario-tag{font-size:10px;color:#9AA3AE;}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="brand">AP CONTROL TOWER<small>AI Invoice Automation Sim</small></div>
    <nav class="nav" id="navTabs">
      <button data-tab="overview" class="active">Overview</button>
      <button data-tab="queue">Invoice Queue <span class="count" id="navCountQueue">0</span></button>
      <button data-tab="vendors">Vendor Master</button>
      <button data-tab="pos">PO Master</button>
      <button data-tab="ledger">Posted Ledger <span class="count" id="navCountLedger">0</span></button>
      <button data-tab="log">Processing Log</button>
    </nav>
    <div class="side-kpis">
      <div><div class="side-kpi-label">Touchless Rate (STP)</div><div class="side-kpi-val mono" id="sideStp">—</div></div>
      <div><div class="side-kpi-label">Extraction Accuracy</div><div class="side-kpi-val mono" id="sideAcc">—</div></div>
      <div><div class="side-kpi-label">Open Exceptions</div><div class="side-kpi-val mono" id="sideExc">0</div></div>
    </div>
  </aside>

  <main>
    <div class="topbar">
      <div>
        <h1>AI-Powered AP Invoice Processing — Live Simulation</h1>
        <p>Synthetic invoices are rendered as images, read by Claude (vision) for data extraction, then run through validation, PO matching, and approval routing — end to end.</p>
      </div>
      <div class="actions">
        <button class="btn" id="btnGenerate">1 · Generate Invoice Batch</button>
        <button class="btn primary" id="btnRun" disabled>2 · Run Full Pipeline</button>
        <button class="btn" id="btnReset">Reset</button>
      </div>
    </div>

    <div class="info-banner" id="statusBanner">No batch generated yet. Click <b>Generate Invoice Batch</b> to create a synthetic set of vendors, purchase orders, and invoices (rendered as images) for this run.</div>

    <div class="rail" id="rail"></div>

    <section class="tab active" id="tab-overview">
      <div class="grid-kpi" id="kpiCards"></div>
      <div class="charts-row">
        <div class="panel"><h3>Invoice Status Breakdown</h3><canvas id="chartStatus" height="220"></canvas></div>
        <div class="panel"><h3>Exceptions by Reason</h3><canvas id="chartExceptions" height="220"></canvas></div>
      </div>
      <div class="panel">
        <h3>Cycle Time — Automated vs. Manual Benchmark</h3>
        <p style="font-size:12px;color:var(--ink-soft);margin-top:-4px;">Manual benchmark is an assumed industry reference point (~12 min/invoice for manual 3-way match), used only to illustrate relative time savings — not a measured figure.</p>
        <canvas id="chartCycle" height="120"></canvas>
      </div>
    </section>

    <section class="tab" id="tab-queue">
      <div class="panel">
        <h3>Invoice Queue</h3>
        <table>
          <thead><tr><th>#</th><th>Vendor</th><th>Invoice No.</th><th>PO No.</th><th>Total</th><th>Status</th><th>Decision</th></tr></thead>
          <tbody id="queueBody"></tbody>
        </table>
      </div>
    </section>

    <section class="tab" id="tab-vendors">
      <div class="panel">
        <h3>Vendor Master</h3>
        <table>
          <thead><tr><th>Vendor</th><th>Category</th><th>GL Code</th><th>Approved</th></tr></thead>
          <tbody id="vendorBody"></tbody>
        </table>
      </div>
    </section>

    <section class="tab" id="tab-pos">
      <div class="panel">
        <h3>Purchase Order Master</h3>
        <table>
          <thead><tr><th>PO Number</th><th>Vendor</th><th>Amount</th><th>GL Code</th><th>Status</th></tr></thead>
          <tbody id="poBody"></tbody>
        </table>
      </div>
    </section>

    <section class="tab" id="tab-ledger">
      <div class="panel">
        <h3>Posted Ledger</h3>
        <table>
          <thead><tr><th>Invoice No.</th><th>Vendor</th><th>GL Code</th><th>Amount</th><th>Approval Type</th><th>Posted At</th></tr></thead>
          <tbody id="ledgerBody"></tbody>
        </table>
      </div>
    </section>

    <section class="tab" id="tab-log">
      <div class="panel"><h3>Processing Log</h3><div id="logBody"></div></div>
    </section>
  </main>
</div>

<div class="modal-overlay hidden" id="modalOverlay">
  <div class="modal">
    <div class="modal-head"><h2 id="modalTitle">Invoice detail</h2><button class="close-x" id="modalClose">✕</button></div>
    <div id="modalBody"></div>
  </div>
</div>

<script>
/* ===================== SYNTHETIC DATA GENERATION ===================== */
const VENDOR_POOL = [
  { name: "Atlas Office Supplies Co.", category: "Office Supplies", glCode: "6100 - Office Supplies", address: "1200 Commerce Way, Dallas, TX 75201" },
  { name: "Meridian Freight & Logistics", category: "Freight & Logistics", glCode: "6210 - Freight & Logistics", address: "88 Harbor Blvd, Newark, NJ 07102" },
  { name: "Nimbus Cloud Services Inc.", category: "IT & Cloud Services", glCode: "6310 - IT & Cloud Services", address: "450 Innovation Drive, Austin, TX 78701" },
  { name: "Sterling Industrial Parts", category: "Raw Materials", glCode: "6610 - Raw Materials", address: "77 Foundry St, Pittsburgh, PA 15222" },
  { name: "Halcyon Marketing Group", category: "Marketing & Advertising", glCode: "6510 - Marketing & Advertising", address: "930 Market St, San Francisco, CA 94103" },
  { name: "Bridgeport Facilities Maintenance", category: "Facilities Maintenance", glCode: "6410 - Facilities Maintenance", address: "15 Distribution Pkwy, Memphis, TN 38118" },
  { name: "Quantum Office Tech", category: "IT & Cloud Services", glCode: "6310 - IT & Cloud Services", address: "260 Enterprise Ave, Charlotte, NC 28202" },
  { name: "Ferro Steel Distributors", category: "Raw Materials", glCode: "6610 - Raw Materials", address: "5 Riverside Plaza, Chicago, IL 60606" },
];
const LINE_ITEM_PHRASES = {
  "Office Supplies": ["A4 Paper Reams", "Toner Cartridges", "Desk Organizers", "Whiteboard Markers", "Filing Folders"],
  "Freight & Logistics": ["Freight Charges - LTL", "Fuel Surcharge", "Warehouse Handling", "Cross-Dock Fee", "Pallet Rental"],
  "IT & Cloud Services": ["Cloud Compute Hours", "SaaS License - Annual", "Storage Subscription", "Support Plan - Tier 2", "API Usage Overage"],
  "Raw Materials": ["Cold Rolled Steel Sheet", "Aluminum Billet", "Industrial Fasteners", "Welding Rods", "Steel Coil"],
  "Marketing & Advertising": ["Digital Ad Spend", "Creative Design Hours", "Social Media Management", "Print Collateral", "Campaign Analytics"],
  "Facilities Maintenance": ["HVAC Service Call", "Janitorial Services", "Pest Control", "Plumbing Repair", "Elevator Maintenance"],
};
const BUYER = { name: "Brightford Manufacturing Inc.", address: "442 Industrial Pkwy, Columbus, OH 43215" };
const BRAND_COLORS = ['#2B4C7E','#7E2B3F','#2B7E63','#7E5C2B','#4B2B7E','#2B6B7E','#7E2B6B','#5C7E2B'];

function rnd(a,b){return Math.random()*(b-a)+a;}
function rndInt(a,b){return Math.floor(rnd(a,b+1));}
function pick(arr){return arr[rndInt(0,arr.length-1)];}
function round2(n){return Math.round(n*100)/100;}
function moneyFmt(n){return '$' + Number(n).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function vendorColor(name){let h=0;for(const c of name)h=(h*31+c.charCodeAt(0))%BRAND_COLORS.length;return BRAND_COLORS[h];}
function randomDateWithin(daysBack){const d=new Date();d.setDate(d.getDate()-rndInt(0,daysBack));return d.toISOString().slice(0,10);}
function addDays(dateStr,days){const d=new Date(dateStr);d.setDate(d.getDate()+days);return d.toISOString().slice(0,10);}

let _idCounter=1,_poCounter=4000;

function buildLineItems(category){
  const n=rndInt(2,4);const phrases=LINE_ITEM_PHRASES[category];const used=new Set();const items=[];
  for(let i=0;i<n;i++){
    let desc; let guard=0;
    do{desc=pick(phrases);guard++;}while(used.has(desc)&&used.size<phrases.length&&guard<10);
    used.add(desc);
    const qty=rndInt(1,10);const unitPrice=round2(rnd(8,150));
    items.push({description:desc,quantity:qty,unitPrice,amount:round2(qty*unitPrice)});
  }
  return items;
}
function totalsFromItems(items,taxRate){
  const subtotal=round2(items.reduce((s,i)=>s+i.amount,0));
  const taxAmount=round2(subtotal*taxRate);
  const total=round2(subtotal+taxAmount);
  return {subtotal,taxAmount,total};
}
function makeBaseInvoice(vendor){
  const taxRate=pick([0,0.05,0.0725,0.08]);
  const lineItems=buildLineItems(vendor.category);
  const {subtotal,taxAmount,total}=totalsFromItems(lineItems,taxRate);
  const invoiceDate=randomDateWithin(20);
  const id="inv_"+_idCounter++;
  return {
    id, vendor:vendor.name, vendorCategory:vendor.category,
    invoiceNumber:"INV-"+vendor.name.slice(0,3).toUpperCase()+"-"+rndInt(10000,99999),
    poNumber:null, invoiceDate, dueDate:addDays(invoiceDate,30), currency:"USD",
    lineItems, taxRate, subtotal, taxAmount, total, scenario:"clean",
    template:pick(["classic","modern","minimal"]), scanNoise:Math.random()<0.2,
    status:"queued", extracted:null, extractionError:null, accuracy:null,
    issues:[], matchResult:null, approval:null, approvalType:null, imageDataUrl:null, postedAt:null,
  };
}
function newPO(vendor,amount){
  return {poNumber:"PO-2026-"+(_poCounter++), vendor:vendor.name, amount:round2(amount), glCode:vendor.glCode, status:"open"};
}
function generateDataset(){
  _idCounter=1;_poCounter=4000;
  const unapprovedIdx=rndInt(0,VENDOR_POOL.length-1);
  const vendorMaster=VENDOR_POOL.map((v,i)=>({...v,approved:i!==unapprovedIdx}));
  const poMaster=[]; const invoices=[];
  const approvedVendors=vendorMaster.filter(v=>v.approved);
  const unapprovedVendor=vendorMaster[unapprovedIdx];
  const plan=["clean","clean","clean","clean","clean","clean","amount_mismatch","amount_mismatch","no_po","no_po","unapproved_vendor","clean"];
  plan.sort(()=>Math.random()-0.5);
  for(const scenario of plan){
    let vendor = scenario==="unapproved_vendor" ? unapprovedVendor : pick(approvedVendors);
    const inv=makeBaseInvoice(vendor);
    inv.scenario=scenario;
    if(scenario==="clean"){
      const po=newPO(vendor,inv.total); poMaster.push(po); inv.poNumber=po.poNumber;
    } else if(scenario==="amount_mismatch"){
      const po=newPO(vendor,inv.total*rnd(0.7,0.85)); poMaster.push(po); inv.poNumber=po.poNumber;
    } else if(scenario==="no_po"){
      inv.poNumber=null;
    } else if(scenario==="unapproved_vendor"){
      const po=newPO(vendor,inv.total); poMaster.push(po); inv.poNumber=po.poNumber;
    }
    invoices.push(inv);
  }
  const cleanOnes=invoices.filter(i=>i.scenario==="clean");
  if(cleanOnes.length){
    const original=cleanOnes[rndInt(0,cleanOnes.length-1)];
    const dup=JSON.parse(JSON.stringify(original));
    dup.id="inv_"+_idCounter++; dup.invoiceDate=addDays(original.invoiceDate,3); dup.dueDate=addDays(dup.invoiceDate,30);
    dup.scenario="duplicate"; dup.template=pick(["classic","modern","minimal"]);
    invoices.push(dup);
  }
  for(let i=0;i<3;i++){const v=pick(approvedVendors);poMaster.push(newPO(v,rnd(500,9000)));}
  return {vendorMaster, poMaster, invoices};
}

/* ===================== VALIDATION & MATCHING ===================== */
const AMOUNT_TOLERANCE_PCT=0.03, NON_PO_AUTO_LIMIT=750, AUTO_APPROVE_LIMIT=5000;

function validateInvoice(extracted, vendorMaster, allInvoices, selfIndex){
  const issues=[];
  if(!extracted.vendor || !extracted.invoiceNumber || extracted.total==null){
    issues.push({code:"MISSING_FIELD", detail:"Required field missing from extracted data."});
  }
  const vendor=vendorMaster.find(v=>v.name.toLowerCase()===String(extracted.vendor).toLowerCase());
  if(!vendor){
    issues.push({code:"UNKNOWN_VENDOR", detail:`Vendor "${extracted.vendor}" not found in vendor master.`});
  } else if(!vendor.approved){
    issues.push({code:"UNAPPROVED_VENDOR", detail:`Vendor "${extracted.vendor}" is not an approved vendor.`});
  }
  const dupIndex=allInvoices.findIndex((other,idx)=>idx!==selfIndex && other.extracted &&
    other.extracted.vendor===extracted.vendor && other.extracted.invoiceNumber===extracted.invoiceNumber);
  if(dupIndex!==-1 && dupIndex<selfIndex){
    issues.push({code:"DUPLICATE_INVOICE", detail:`Matches earlier invoice #${dupIndex+1} with same vendor + invoice number.`});
  }
  return issues;
}
function matchInvoice(extracted, poMaster){
  if(!extracted.poNumber){
    if(extracted.total<=NON_PO_AUTO_LIMIT) return {result:"NON_PO_AUTO", detail:"No PO referenced; amount under non-PO auto-approval limit."};
    return {result:"NON_PO_MANUAL", detail:"No PO referenced; amount requires manual review."};
  }
  const po=poMaster.find(p=>p.poNumber===extracted.poNumber);
  if(!po) return {result:"PO_NOT_FOUND", detail:`PO "${extracted.poNumber}" not found in PO master.`};
  if(po.vendor.toLowerCase()!==String(extracted.vendor).toLowerCase()) return {result:"VENDOR_MISMATCH", detail:`PO is registered to "${po.vendor}", not "${extracted.vendor}".`};
  const variance=Math.abs(extracted.total-po.amount)/po.amount;
  if(variance<=AMOUNT_TOLERANCE_PCT) return {result:"MATCHED", detail:`Within tolerance (${(variance*100).toFixed(1)}% variance).`, po, variance};
  return {result:"AMOUNT_VARIANCE", detail:`${(variance*100).toFixed(1)}% variance exceeds ${(AMOUNT_TOLERANCE_PCT*100)}% tolerance.`, po, variance};
}
function decideApproval(issues, matchResult, total){
  if(issues.length>0) return {decision:"EXCEPTION", reason:issues.map(i=>i.code).join(", ")};
  if(matchResult.result==="MATCHED" && total<AUTO_APPROVE_LIMIT) return {decision:"AUTO_APPROVED", reason:"Matched + under auto-approve limit."};
  if(matchResult.result==="MATCHED") return {decision:"PENDING_APPROVAL", reason:"Matched but exceeds auto-approve limit."};
  if(matchResult.result==="NON_PO_AUTO") return {decision:"AUTO_APPROVED", reason:"Non-PO, low value."};
  if(matchResult.result==="NON_PO_MANUAL") return {decision:"PENDING_APPROVAL", reason:"Non-PO, requires review."};
  return {decision:"EXCEPTION", reason:matchResult.detail};
}
function scoreAccuracy(extracted, inv){
  let correct=0; const total=5;
  if(extracted.vendor && extracted.vendor.toLowerCase()===inv.vendor.toLowerCase()) correct++;
  if(extracted.invoiceNumber===inv.invoiceNumber) correct++;
  const poOk=(extracted.poNumber||null)===(inv.poNumber||null);
  if(poOk) correct++;
  if(extracted.invoiceDate===inv.invoiceDate) correct++;
  if(typeof extracted.total==="number" && Math.abs(extracted.total-inv.total)<0.01) correct++;
  return Math.round((correct/total)*100);
}

/* ===================== CANVAS INVOICE RENDERING ===================== */
function txt(ctx,str,x,y,{font="14px Arial",color="#111",align="left"}={}){
  ctx.font=font; ctx.fillStyle=color; ctx.textAlign=align; ctx.fillText(str,x,y);
}
function drawTableCommon(ctx, items, startY, cols){
  let y=startY;
  ctx.font="bold 13px Arial"; ctx.fillStyle="#333";
  ctx.textAlign="left"; ctx.fillText("DESCRIPTION", cols.desc, y);
  ctx.textAlign="right";
  ctx.fillText("QTY", cols.qty, y); ctx.fillText("UNIT PRICE", cols.price, y); ctx.fillText("AMOUNT", cols.amount, y);
  y+=10; ctx.strokeStyle="#999"; ctx.beginPath(); ctx.moveTo(cols.desc-10,y); ctx.lineTo(cols.amount+10,y); ctx.stroke();
  y+=26;
  ctx.font="13px Arial"; ctx.fillStyle="#222";
  items.forEach(it=>{
    ctx.textAlign="left"; ctx.fillText(it.description, cols.desc, y);
    ctx.textAlign="right";
    ctx.fillText(String(it.quantity), cols.qty, y);
    ctx.fillText(moneyFmt(it.unitPrice), cols.price, y);
    ctx.fillText(moneyFmt(it.amount), cols.amount, y);
    y+=28;
  });
  return y;
}
function drawClassic(ctx, inv, vendor){
  txt(ctx, vendor.name, 60, 70, {font:"bold 28px Georgia", color:"#111"});
  txt(ctx, vendor.address, 60, 94, {font:"13px Arial", color:"#555"});
  txt(ctx, "INVOICE", 940, 70, {font:"bold 26px Georgia", align:"right"});
  txt(ctx, "Invoice #: "+inv.invoiceNumber, 940, 96, {font:"13px Arial", align:"right"});
  txt(ctx, "Date: "+inv.invoiceDate, 940, 114, {font:"13px Arial", align:"right"});
  txt(ctx, "Due: "+inv.dueDate, 940, 132, {font:"13px Arial", align:"right"});
  txt(ctx, "PO #: "+(inv.poNumber||"N/A"), 940, 150, {font:"13px Arial", align:"right"});
  ctx.strokeStyle="#ccc"; ctx.beginPath(); ctx.moveTo(60,175); ctx.lineTo(940,175); ctx.stroke();
  txt(ctx, "BILL TO", 60, 205, {font:"bold 11px Arial", color:"#888"});
  txt(ctx, BUYER.name, 60, 224, {font:"14px Arial"});
  txt(ctx, BUYER.address, 60, 242, {font:"13px Arial", color:"#555"});
  const endY=drawTableCommon(ctx, inv.lineItems, 300, {desc:60, qty:560, price:760, amount:940});
  let y=endY+20;
  ctx.strokeStyle="#ccc"; ctx.beginPath(); ctx.moveTo(660,y-14); ctx.lineTo(940,y-14); ctx.stroke();
  txt(ctx,"Subtotal", 760, y, {font:"13px Arial", align:"right"}); txt(ctx,moneyFmt(inv.subtotal),940,y,{font:"13px Arial",align:"right"}); y+=24;
  txt(ctx,"Tax", 760, y, {font:"13px Arial", align:"right"}); txt(ctx,moneyFmt(inv.taxAmount),940,y,{font:"13px Arial",align:"right"}); y+=28;
  txt(ctx,"TOTAL", 760, y, {font:"bold 17px Arial", align:"right"}); txt(ctx,moneyFmt(inv.total),940,y,{font:"bold 17px Arial",align:"right"});
  txt(ctx, "Payment due within 30 days. Thank you for your business.", 60, 1240, {font:"11px Arial", color:"#999"});
}
function drawModern(ctx, inv, vendor){
  const c=vendorColor(vendor.name);
  ctx.fillStyle=c; ctx.fillRect(0,0,1000,140);
  txt(ctx, vendor.name, 50, 65, {font:"bold 28px Arial", color:"#fff"});
  txt(ctx, vendor.address, 50, 92, {font:"13px Arial", color:"rgba(255,255,255,.85)"});
  txt(ctx, "INVOICE", 950, 75, {font:"bold 26px Arial", color:"#fff", align:"right"});
  const meta=[["Invoice #",inv.invoiceNumber],["Invoice Date",inv.invoiceDate],["Due Date",inv.dueDate],["PO Number",inv.poNumber||"N/A"]];
  let mx=50;
  meta.forEach(([k,v])=>{
    txt(ctx,k.toUpperCase(),mx,185,{font:"10px Arial",color:"#888"});
    txt(ctx,String(v),mx,208,{font:"bold 14px Arial",color:"#111"});
    mx+=235;
  });
  txt(ctx, "BILL TO  "+BUYER.name+", "+BUYER.address, 50, 250, {font:"12px Arial", color:"#666"});
  ctx.fillStyle="#F1F3EF"; ctx.fillRect(50,290,900,32);
  const endY=drawTableCommon(ctx, inv.lineItems, 312, {desc:65, qty:560, price:760, amount:935});
  let y=endY+16;
  ctx.fillStyle=c; ctx.fillRect(620,y-6,330,46);
  txt(ctx,"TOTAL DUE", 645, y+22, {font:"bold 14px Arial", color:"#fff"});
  txt(ctx, moneyFmt(inv.total), 935, y+22, {font:"bold 20px Arial", color:"#fff", align:"right"});
  txt(ctx, `Subtotal ${moneyFmt(inv.subtotal)}   ·   Tax ${moneyFmt(inv.taxAmount)}`, 935, y-16, {font:"12px Arial", color:"#666", align:"right"});
}
function drawMinimal(ctx, inv, vendor){
  txt(ctx, vendor.name, 60, 80, {font:"22px Courier New"});
  txt(ctx, "Invoice", 60, 106, {font:"14px Courier New", color:"#555"});
  txt(ctx, `Invoice #: ${inv.invoiceNumber}    Date: ${inv.invoiceDate}    Due: ${inv.dueDate}    PO: ${inv.poNumber||"N/A"}`, 60, 140, {font:"13px Courier New"});
  txt(ctx, `Bill To: ${BUYER.name}, ${BUYER.address}`, 60, 164, {font:"13px Courier New", color:"#555"});
  ctx.strokeStyle="#000"; ctx.beginPath(); ctx.moveTo(60,185); ctx.lineTo(940,185); ctx.stroke();
  let y=225;
  ctx.font="13px Courier New"; ctx.fillStyle="#111";
  inv.lineItems.forEach(it=>{
    ctx.textAlign="left"; ctx.fillText(`${it.description}`, 60, y);
    ctx.textAlign="right";
    ctx.fillText(`${it.quantity} x ${moneyFmt(it.unitPrice)} = ${moneyFmt(it.amount)}`, 940, y);
    y+=30;
  });
  y+=14;
  ctx.textAlign="right";
  ctx.font="13px Courier New"; ctx.fillText(`Subtotal: ${moneyFmt(inv.subtotal)}`,940,y); y+=20;
  ctx.fillText(`Tax: ${moneyFmt(inv.taxAmount)}`,940,y); y+=24;
  ctx.font="bold 16px Courier New"; ctx.fillText(`Total: ${moneyFmt(inv.total)}`,940,y);
}
function applyScanNoise(ctx,w,h){
  ctx.save();
  ctx.fillStyle='rgba(120,120,120,0.06)'; ctx.fillRect(0,0,w,h);
  ctx.strokeStyle='rgba(0,0,0,0.05)';
  for(let i=0;i<6;i++){const y=Math.random()*h; ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.lineWidth=1; ctx.stroke();}
  for(let i=0;i<350;i++){ctx.fillStyle='rgba(0,0,0,'+(Math.random()*0.04)+')'; ctx.fillRect(Math.random()*w, Math.random()*h, 1, 1);}
  ctx.restore();
}
function renderInvoiceCanvas(inv, vendor){
  const canvas=document.createElement('canvas');
  canvas.width=1000; canvas.height=1294;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle="#ffffff"; ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.save();
  if(inv.scanNoise){
    const angle=(Math.random()*4-2)*Math.PI/180;
    ctx.translate(canvas.width/2,canvas.height/2); ctx.rotate(angle); ctx.translate(-canvas.width/2,-canvas.height/2);
  }
  if(inv.template==="classic") drawClassic(ctx, inv, vendor);
  else if(inv.template==="modern") drawModern(ctx, inv, vendor);
  else drawMinimal(ctx, inv, vendor);
  ctx.restore();
  if(inv.scanNoise) applyScanNoise(ctx, canvas.width, canvas.height);
  return canvas;
}

/* ===================== EXTRACTION (Claude vision) ===================== */
async function extractInvoiceData(imageDataUrl){
  const base64=imageDataUrl.split(',')[1];
  const prompt=`You are an automated invoice data extraction system used in an Accounts Payable pipeline. Extract structured data from this invoice image. Return ONLY a single valid JSON object, with no markdown formatting, no code fences, and no commentary. Use exactly this schema: {"vendor": string, "invoiceNumber": string, "poNumber": string or null, "invoiceDate": "YYYY-MM-DD", "dueDate": "YYYY-MM-DD" or null, "currency": string, "lineItems": [{"description": string, "quantity": number, "unitPrice": number, "amount": number}], "subtotal": number, "taxAmount": number, "total": number}. If a field is not present on the invoice, use null. Numbers must be plain numbers without currency symbols or commas.`;
  const response=await fetch("https://api.anthropic.com/v1/messages", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({
      model:"claude-sonnet-4-6",
      max_tokens:1000,
      messages:[{role:"user", content:[
        {type:"image", source:{type:"base64", media_type:"image/png", data: base64}},
        {type:"text", text: prompt}
      ]}]
    })
  });
  if(!response.ok) throw new Error("API error "+response.status);
  const data=await response.json();
  const textBlock=(data.content||[]).find(b=>b.type==="text");
  if(!textBlock) throw new Error("No text in response");
  const clean=textBlock.text.replace(/```json|```/g,"").trim();
  return JSON.parse(clean);
}

/* ===================== STATE & PIPELINE ===================== */
let STATE={vendorMaster:[], poMaster:[], invoices:[], log:[], running:false};

function log(msg){
  STATE.log.unshift({time:new Date().toLocaleTimeString(), msg});
  renderLog();
}

async function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

async function processInvoice(inv, idx){
  inv.status="processing"; renderAll();
  try{
    const extracted=await extractInvoiceData(inv.imageDataUrl);
    inv.extracted=extracted;
    inv.accuracy=scoreAccuracy(extracted, inv);
    log(`Extracted invoice ${idx+1} (${inv.template} template${inv.scanNoise?", scan noise":""}) — field accuracy ${inv.accuracy}%`);
  }catch(e){
    inv.extractionError=String(e.message||e);
    log(`Extraction FAILED for invoice ${idx+1}: ${inv.extractionError}`);
    inv.status="exception"; inv.issues=[{code:"EXTRACTION_FAILED", detail: inv.extractionError}];
    inv.approval={decision:"EXCEPTION", reason:"Extraction failed"};
    renderAll(); return;
  }
  const issues=validateInvoice(inv.extracted, STATE.vendorMaster, STATE.invoices, idx);
  const matchResult=matchInvoice(inv.extracted, STATE.poMaster);
  const approval=decideApproval(issues, matchResult, inv.extracted.total);
  inv.issues=issues; inv.matchResult=matchResult; inv.approval=approval;
  if(approval.decision==="EXCEPTION"){
    inv.status="exception";
    log(`Invoice ${idx+1}: EXCEPTION — ${approval.reason}`);
  } else if(approval.decision==="AUTO_APPROVED"){
    inv.status="posted"; inv.approvalType="auto"; inv.postedAt=new Date().toLocaleString();
    log(`Invoice ${idx+1}: auto-approved and posted (${matchResult.result}).`);
  } else {
    inv.status="pending_approval";
    log(`Invoice ${idx+1}: routed to pending approval — ${approval.reason}`);
  }
  renderAll();
}

async function runFullPipeline(){
  if(STATE.running) return;
  STATE.running=true;
  document.getElementById('btnRun').disabled=true;
  for(let i=0;i<STATE.invoices.length;i++){
    const inv=STATE.invoices[i];
    if(inv.status!=="queued") continue;
    await processInvoice(inv, i);
    await sleep(250);
  }
  STATE.running=false;
  document.getElementById('btnRun').disabled = STATE.invoices.every(i=>i.status!=="queued");
  log("Pipeline run complete.");
}

function manualApprove(invId){
  const inv=STATE.invoices.find(i=>i.id===invId);
  if(!inv) return;
  inv.status="posted"; inv.approvalType = inv.issues && inv.issues.length ? "manual_override" : "manual";
  inv.postedAt=new Date().toLocaleString();
  log(`Invoice manually approved and posted (${inv.invoiceNumber||inv.id}).`);
  closeModal(); renderAll();
}
async function retryExtraction(invId){
  const idx=STATE.invoices.findIndex(i=>i.id===invId);
  if(idx===-1) return;
  STATE.invoices[idx].status="queued"; STATE.invoices[idx].extractionError=null;
  closeModal();
  await processInvoice(STATE.invoices[idx], idx);
}

/* ===================== RENDERING ===================== */
const STAGES=[
  {key:"queued", label:"Queued", cls:"st-queued"},
  {key:"processing", label:"Processing", cls:"st-processing"},
  {key:"exception", label:"Exception", cls:"st-exception"},
  {key:"pending_approval", label:"Pending Approval", cls:"st-pending"},
  {key:"posted", label:"Posted", cls:"st-posted"},
];
function countByStatus(status){return STATE.invoices.filter(i=>i.status===status).length;}

function renderRail(){
  const rail=document.getElementById('rail');
  rail.innerHTML="";
  STAGES.forEach((s,idx)=>{
    const count=countByStatus(s.key);
    const node=document.createElement('div');
    node.className="rail-node "+s.cls+(count>0?" active":"");
    node.innerHTML=`<div class="rail-dot">${count}</div><div class="rail-label">${s.label}</div>`;
    rail.appendChild(node);
    if(idx<STAGES.length-1){
      const line=document.createElement('div'); line.className="rail-line"; rail.appendChild(line);
    }
  });
}

function pillFor(status){
  const map={queued:"Queued",processing:"Processing",exception:"Exception",pending_approval:"Pending Approval",posted:"Posted"};
  return `<span class="pill pill-${status}">${map[status]||status}</span>`;
}

function renderKPIs(){
  const total=STATE.invoices.length;
  const posted=STATE.invoices.filter(i=>i.status==="posted");
  const autoPosted=posted.filter(i=>i.approvalType==="auto");
  const stp= total? Math.round((autoPosted.length/total)*100):0;
  const accuracies=STATE.invoices.filter(i=>i.accuracy!=null).map(i=>i.accuracy);
  const avgAcc= accuracies.length? Math.round(accuracies.reduce((a,b)=>a+b,0)/accuracies.length):null;
  const openExceptions=countByStatus("exception");
  const totalPosted=posted.reduce((s,i)=>s+(i.extracted?i.extracted.total:i.total),0);

  document.getElementById('sideStp').textContent= total? stp+"%":"—";
  document.getElementById('sideAcc').textContent= avgAcc!=null? avgAcc+"%":"—";
  document.getElementById('sideExc').textContent= openExceptions;

  const cards=[
    {label:"Invoices in Batch", val:total, sub:`${posted.length} posted so far`},
    {label:"Touchless (STP) Rate", val: total? stp+"%":"—", sub:`${autoPosted.length} auto-approved & posted`},
    {label:"Extraction Accuracy", val: avgAcc!=null? avgAcc+"%":"—", sub:"Avg. field-match vs. ground truth"},
    {label:"Total Posted Value", val: moneyFmt(totalPosted), sub:`${posted.length} invoices`},
    {label:"Open Exceptions", val: openExceptions, sub:"Need resolution"},
    {label:"Pending Approval", val: countByStatus("pending_approval"), sub:"Awaiting human sign-off"},
  ];
  document.getElementById('kpiCards').innerHTML=cards.map(c=>
    `<div class="kpi-card"><div class="label">${c.label}</div><div class="val">${c.val}</div><div class="sub">${c.sub}</div></div>`
  ).join("");
}

let charts={};
function renderCharts(){
  if(!window.Chart) return;
  const statusCounts=STAGES.map(s=>countByStatus(s.key));
  const ctx1=document.getElementById('chartStatus');
  if(charts.status) charts.status.destroy();
  charts.status=new Chart(ctx1, {type:'doughnut', data:{labels:STAGES.map(s=>s.label), datasets:[{data:statusCounts, backgroundColor:['#9AA3AE','#1F6F78','#A84432','#B8853A','#4F7A56']}]}, options:{plugins:{legend:{position:'bottom', labels:{boxWidth:10,font:{size:11}}}}}});

  const reasonTally={};
  STATE.invoices.forEach(inv=>{
    (inv.issues||[]).forEach(is=>{reasonTally[is.code]=(reasonTally[is.code]||0)+1;});
    if(inv.matchResult && ["AMOUNT_VARIANCE","PO_NOT_FOUND","VENDOR_MISMATCH"].includes(inv.matchResult.result)){
      reasonTally[inv.matchResult.result]=(reasonTally[inv.matchResult.result]||0)+1;
    }
  });
  const ctx2=document.getElementById('chartExceptions');
  if(charts.exc) charts.exc.destroy();
  charts.exc=new Chart(ctx2, {type:'bar', data:{labels:Object.keys(reasonTally), datasets:[{data:Object.values(reasonTally), backgroundColor:'#A84432'}]}, options:{plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, ticks:{precision:0}}}}});

  const manualMinutes=12, autoSeconds=8;
  const posted=STATE.invoices.filter(i=>i.status==="posted");
  const ctx3=document.getElementById('chartCycle');
  if(charts.cycle) charts.cycle.destroy();
  charts.cycle=new Chart(ctx3, {type:'bar', data:{
    labels:["Manual process (assumed benchmark)","Automated pipeline (this run)"],
    datasets:[{data:[manualMinutes, (autoSeconds/60).toFixed(2)], backgroundColor:['#B8853A','#1F6F78']}]
  }, options:{indexAxis:'y', plugins:{legend:{display:false}}, scales:{x:{title:{display:true,text:'Minutes per invoice'}}}}});
}

function renderQueueTable(){
  const body=document.getElementById('queueBody');
  if(!STATE.invoices.length){ body.innerHTML=`<tr><td colspan="7" class="empty">No invoices yet — generate a batch to begin.</td></tr>`; document.getElementById('navCountQueue').textContent="0"; return; }
  document.getElementById('navCountQueue').textContent=STATE.invoices.filter(i=>i.status==="queued"||i.status==="processing").length;
  body.innerHTML=STATE.invoices.map((inv,idx)=>{
    const decision= inv.approval? inv.approval.decision.replace("_"," ") : "—";
    return `<tr class="clickable" onclick="openModal('${inv.id}')">
      <td>${idx+1}</td>
      <td>${inv.vendor}<div class="scenario-tag">scenario: ${inv.scenario}</div></td>
      <td class="mono">${inv.extracted? inv.extracted.invoiceNumber : inv.invoiceNumber}</td>
      <td class="mono">${(inv.extracted? inv.extracted.poNumber : inv.poNumber) || "—"}</td>
      <td class="mono">${moneyFmt(inv.extracted? inv.extracted.total : inv.total)}</td>
      <td>${pillFor(inv.status)}</td>
      <td>${decision}</td>
    </tr>`;
  }).join("");
}
function renderVendorTable(){
  const body=document.getElementById('vendorBody');
  if(!STATE.vendorMaster.length){ body.innerHTML=`<tr><td colspan="4" class="empty">No vendor data yet.</td></tr>`; return; }
  body.innerHTML=STATE.vendorMaster.map(v=>`<tr><td>${v.name}</td><td>${v.category}</td><td class="mono">${v.glCode}</td><td>${v.approved? '<span class="pill pill-posted">Approved</span>':'<span class="pill pill-exception">Not Approved</span>'}</td></tr>`).join("");
}
function renderPOTable(){
  const body=document.getElementById('poBody');
  if(!STATE.poMaster.length){ body.innerHTML=`<tr><td colspan="5" class="empty">No PO data yet.</td></tr>`; return; }
  body.innerHTML=STATE.poMaster.map(p=>`<tr><td class="mono">${p.poNumber}</td><td>${p.vendor}</td><td class="mono">${moneyFmt(p.amount)}</td><td class="mono">${p.glCode}</td><td>${p.status}</td></tr>`).join("");
}
function renderLedgerTable(){
  const body=document.getElementById('ledgerBody');
  const posted=STATE.invoices.filter(i=>i.status==="posted");
  document.getElementById('navCountLedger').textContent=posted.length;
  if(!posted.length){ body.innerHTML=`<tr><td colspan="6" class="empty">Nothing posted yet.</td></tr>`; return; }
  body.innerHTML=posted.map(inv=>{
    const vendor=STATE.vendorMaster.find(v=>v.name===inv.vendor);
    return `<tr><td class="mono">${inv.extracted? inv.extracted.invoiceNumber: inv.invoiceNumber}</td><td>${inv.vendor}</td><td class="mono">${vendor? vendor.glCode:"—"}</td><td class="mono">${moneyFmt(inv.extracted? inv.extracted.total: inv.total)}</td><td>${inv.approvalType}</td><td>${inv.postedAt||"—"}</td></tr>`;
  }).join("");
}
function renderLog(){
  const body=document.getElementById('logBody');
  if(!STATE.log.length){ body.innerHTML=`<div class="empty">No activity yet.</div>`; return; }
  body.innerHTML=STATE.log.map(l=>`<div class="log-row"><span class="log-time mono">${l.time}</span>${l.msg}</div>`).join("");
}
function renderStatusBanner(){
  const el=document.getElementById('statusBanner');
  if(!STATE.invoices.length) return;
  const queued=countByStatus("queued");
  if(queued===STATE.invoices.length){
    el.innerHTML=`Batch ready: <b>${STATE.invoices.length} invoices</b>, ${STATE.vendorMaster.length} vendors, ${STATE.poMaster.length} purchase orders. Click <b>Run Full Pipeline</b> to extract, validate, match, and route each invoice.`;
  } else if(STATE.running){
    el.innerHTML=`Pipeline running — processing invoices through Claude vision extraction, validation, and PO matching...`;
  } else {
    el.innerHTML=`Run complete. Review exceptions and pending approvals in the Invoice Queue, or check Overview for KPIs.`;
  }
}
function renderAll(){
  renderRail(); renderKPIs(); renderCharts(); renderQueueTable(); renderVendorTable(); renderPOTable(); renderLedgerTable(); renderLog(); renderStatusBanner();
}

/* ===================== MODAL ===================== */
function openModal(invId){
  const inv=STATE.invoices.find(i=>i.id===invId);
  if(!inv) return;
  document.getElementById('modalTitle').textContent=`${inv.vendor} — ${inv.invoiceNumber}`;
  const ext=inv.extracted;
  function diffRow(label, groundTruth, extractedVal){
    const ok = extractedVal===undefined ? false : String(groundTruth)===String(extractedVal);
    return `<div class="kv"><b>${label}</b><span class="${ext? (ok?'diff-ok':'diff-bad'):''}">${ext? (extractedVal===null||extractedVal===undefined?'null':extractedVal) : '<i>not yet extracted</i>'}</span></div>`;
  }
  let body = `<div class="modal-grid">
    <div><img src="${inv.imageDataUrl}" alt="invoice image"/></div>
    <div>
      <h3 style="font-size:13px;margin-top:0;">Extracted vs. Ground Truth</h3>
      ${diffRow("Vendor", inv.vendor, ext?ext.vendor:undefined)}
      ${diffRow("Invoice #", inv.invoiceNumber, ext?ext.invoiceNumber:undefined)}
      ${diffRow("PO #", inv.poNumber||"null", ext?(ext.poNumber||"null"):undefined)}
      ${diffRow("Invoice Date", inv.invoiceDate, ext?ext.invoiceDate:undefined)}
      ${diffRow("Total", inv.total, ext?ext.total:undefined)}
      ${inv.accuracy!=null? `<p style="font-size:12px;margin-top:8px;">Field accuracy: <b>${inv.accuracy}%</b></p>`:""}
      <h3 style="font-size:13px;margin-top:16px;">Status</h3>
      <p style="font-size:12.5px;">${pillFor(inv.status)} ${inv.matchResult? " — "+inv.matchResult.detail : ""}</p>
      ${inv.issues && inv.issues.length? `<div>${inv.issues.map(is=>`<div class="issue-row"><b>${is.code}</b>: ${is.detail}</div>`).join("")}</div>` : ""}
      ${inv.extractionError? `<div class="issue-row"><b>EXTRACTION ERROR</b>: ${inv.extractionError}</div><button class="btn small" onclick="retryExtraction('${inv.id}')">Retry Extraction</button>`:""}
      ${(inv.status==="exception"||inv.status==="pending_approval")? `<div style="margin-top:12px;"><button class="btn primary small" onclick="manualApprove('${inv.id}')">Approve &amp; Post Manually</button></div>`:""}
    </div>
  </div>`;
  document.getElementById('modalBody').innerHTML=body;
  document.getElementById('modalOverlay').classList.remove('hidden');
}
function closeModal(){document.getElementById('modalOverlay').classList.add('hidden');}
document.getElementById('modalClose').onclick=closeModal;
document.getElementById('modalOverlay').onclick=(e)=>{if(e.target.id==='modalOverlay') closeModal();};

/* ===================== TABS ===================== */
document.getElementById('navTabs').addEventListener('click', (e)=>{
  const btn=e.target.closest('button'); if(!btn) return;
  document.querySelectorAll('#navTabs button').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+btn.dataset.tab).classList.add('active');
});

/* ===================== MAIN ACTIONS ===================== */
document.getElementById('btnGenerate').onclick=()=>{
  const {vendorMaster, poMaster, invoices} = generateDataset();
  invoices.forEach(inv=>{
    const vendor=vendorMaster.find(v=>v.name===inv.vendor);
    const canvas=renderInvoiceCanvas(inv, vendor);
    inv.imageDataUrl=canvas.toDataURL('image/png');
  });
  STATE={vendorMaster, poMaster, invoices, log:[], running:false};
  log(`Generated new batch: ${invoices.length} invoices, ${vendorMaster.length} vendors, ${poMaster.length} POs.`);
  document.getElementById('btnRun').disabled=false;
  renderAll();
};
document.getElementById('btnRun').onclick=runFullPipeline;
document.getElementById('btnReset').onclick=()=>{
  STATE={vendorMaster:[], poMaster:[], invoices:[], log:[], running:false};
  document.getElementById('btnRun').disabled=true;
  renderAll();
  document.getElementById('statusBanner').innerHTML="No batch generated yet. Click <b>Generate Invoice Batch</b> to create a synthetic set of vendors, purchase orders, and invoices (rendered as images) for this run.";
};

renderAll();
</script>
</body>
</html>
