<style>
    /* =====================================
   ULTIMATE BRIGHT FAIRY TALE THEME
   ===================================== */

    /* ===== BACKGROUND SKY ===== */
    body {
        background: linear-gradient(135deg,
                #ffdee9 0%,
                #b5fffc 25%,
                #c9b6ff 50%,
                #ffe29f 75%,
                #ffb7ce 100%) !important;
        background-size: 400% 400%;
        animation: rainbowSky 20s ease infinite;
        font-family: "Georgia", serif !important;
        color: #5a3e85 !important;
        overflow-x: hidden;
    }

    @keyframes rainbowSky {
        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }
    }

    /* ===== FLOATING MAGIC SPARKLES ===== */
    body::after {
        content: "";
        position: fixed;
        width: 200%;
        height: 200%;
        background-image: radial-gradient(white 2px, transparent 2px);
        background-size: 60px 60px;
        opacity: 0.3;
        animation: sparkleMove 30s linear infinite;
        pointer-events: none;
    }

    @keyframes sparkleMove {
        from {
            transform: translateY(0);
        }

        to {
            transform: translateY(-200px);
        }
    }

    /* ===== TOP BAR ===== */
    md-toolbar {
        background: linear-gradient(90deg, #ff9a9e, #fad0c4) !important;
        color: #7a3e9d !important;
        font-weight: bold;
        letter-spacing: 2px;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    }

    /* ===== CARD STYLE ===== */
    .nr-dashboard-card {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px);
        border-radius: 25px !important;
        border: 2px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.8);
        transition: all 0.4s ease;
    }

    .nr-dashboard-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px rgba(255, 255, 255, 1);
    }

    /* ===== CARD TITLE ===== */
    .nr-dashboard-cardtitle {
        color: #ff69b4 !important;
        font-weight: bold;
        font-size: 20px !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 1);
    }

    /* ===== GAUGE TEXT ===== */
    .nr-dashboard-gauge text {
        fill: #8e44ad !important;
        font-weight: bold;
    }

    /* ===== LED ===== */
    .nr-dashboard-ui_led div {
        box-shadow: 0 0 20px currentColor !important;
    }

    /* ===== BUTTON GEM STYLE ===== */
    md-button {
        border-radius: 25px !important;
        background: linear-gradient(45deg, #ff9a9e, #a18cd1, #fbc2eb) !important;
        color: #fff !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }

    md-button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 40px rgba(255, 255, 255, 1);
    }

    /* ===== CHART AREA ===== */
    .nr-dashboard-chart {
        background: rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px;
        padding: 10px;
    }

    /* ===== TEXT ===== */
    .nr-dashboard-text {
        font-size: 17px !important;
        color: #5a3e85 !important;
    }

    /* ===== SOFT CLOUD EFFECT ===== */
    body::before {
        content: "";
        position: fixed;
        width: 300px;
        height: 150px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        filter: blur(40px);
        top: 20%;
        left: 10%;
        animation: cloudFloat 40s infinite linear;
        pointer-events: none;
    }

    @keyframes cloudFloat {
        0% {
            transform: translateX(0);
        }

        100% {
            transform: translateX(100vw);
        }
    }
</style>