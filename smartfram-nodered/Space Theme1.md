<style>
    /* ===============================
   SOFT ENCHANTED FAIRY THEME v2
=============================== */
 
    /* ===== BACKGROUND ===== */
    body {
        background: linear-gradient(135deg, #f6d8ff 0%, #c8f7ff 40%, #ffe7c4 100%) !important;
        font-family: "Georgia", serif !important;
        color: #4b3a5a !important;
    }
 
    /* Sparkle overlay */
    body::before {
        content: "";
        position: fixed;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(rgba(255, 255, 255, 0.6) 1px, transparent 1px);
        background-size: 25px 25px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.3;
    }
 
    /* ===== TOP BAR ===== */
    md-toolbar {
        background: linear-gradient(90deg, #ffb6e6, #b8f0ff) !important;
        color: #5a2d82 !important;
        font-weight: bold;
        letter-spacing: 1px;
        box-shadow: 0 3px 15px rgba(255, 180, 255, 0.4);
    }
 
    /* ===== CARD STYLE (โปร่ง) ===== */
    .nr-dashboard-card {
        background: rgba(243, 183, 214, 0.8) !important;
        backdrop-filter: blur(12px);
        border-radius: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 10px 35px rgba(180, 150, 255, 0.25);
        transition: all 0.3s ease;
    }
 
    /* Hover glow */
    .nr-dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 45px rgba(255, 150, 220, 0.35);
    }
 
    /* ===== CARD TITLE ===== */
    .nr-dashboard-cardtitle {
        color: #b03aff !important;
        font-weight: bold;
        font-size: 18px !important;
        text-shadow: 0 0 6px rgba(255, 255, 255, 0.8);
    }
 
    /* ===== GAUGE ===== */
    .nr-dashboard-gauge text {
        fill: #7a3cff !important;
        font-weight: bold;
    }
 
    /* ===== CONTROL BARS (เรืองแสงแทนสีเทา) ===== */
    .nr-dashboard-switch,
    .nr-dashboard-ui_switch,
    .nr-dashboard-template {
        background: rgba(255, 255, 255, 0.4) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(8px);
    }
 
    /* ===== LED GLOW ===== */
    .nr-dashboard-ui_led div {
        box-shadow: 0 0 15px currentColor !important;
    }
 
    /* ===== BUTTON ===== */
    md-button {
        border-radius: 25px !important;
        background: linear-gradient(45deg, #ff6ec4, #7873f5) !important;
        color: white !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        box-shadow: 0 6px 20px rgba(255, 100, 200, 0.4);
        transition: 0.3s ease;
    }
 
    md-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(255, 100, 220, 0.6);
    }
 
    /* ===== CHART AREA (เทาจาง) ===== */
    .nr-dashboard-chart {
        background: rgba(243, 183, 214, 0.8) !important;
        border-radius: 20px;
        padding: 15px;
        backdrop-filter: blur(10px);
    }
 
    /* ===== TEXT ===== */
    .nr-dashboard-text {
        font-size: 16px !important;
        color: #5a2d82 !important;
    }
 
    /* ===== REMOVE DARK GREY BLOCK ===== */
    .nr-dashboard-cardcontainer {
        background: transparent !important;
    }
 
    /* ===== RESET BUTTON  ===== */
    .nr-dashboard-button button {
        background: linear-gradient(45deg, #ff5f6d, #ffc371) !important;
        border-radius: 20px !important;
        font-weight: bold;
    }
</style>