// Dashboard JavaScript para ACA 3.0

// Auto-refresh cada 30 segundos
let autoRefreshInterval;

function startAutoRefresh() {
    autoRefreshInterval = setInterval(() => {
        location.reload();
    }, 30000); // 30 segundos
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
}

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard ACA 3.0 cargado');
    
    // Iniciar auto-refresh
    startAutoRefresh();
    
    // Agregar eventos a botones
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            location.reload();
        });
    }
    
    // Toggle auto-refresh
    const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('change', function() {
            if (this.checked) {
                startAutoRefresh();
            } else {
                stopAutoRefresh();
            }
        });
    }
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Implementar notificaciones toast
    console.log(`${type.toUpperCase()}: ${message}`);
}

// Función para formato de números
function formatNumber(num) {
    return new Intl.NumberFormat('es-CL').format(num);
}
