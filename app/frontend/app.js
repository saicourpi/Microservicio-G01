// =========================================================================
// PARTE 1: CARGA DINÁMICA DE UBICACIONES
// =========================================================================

let jerarquiaUbicaciones = {};
const baseUrl = 'http://10.47.102.216:8000/api';

window.addEventListener('DOMContentLoaded', async () => {
    try {
        const respuesta = await fetch(`${baseUrl}/ubicaciones/jerarquia`);
        jerarquiaUbicaciones = await respuesta.json();

        const selectDpto = document.getElementById('dpto');
        selectDpto.innerHTML = '<option value="">-- Seleccione Departamento --</option>';
        
        Object.keys(jerarquiaUbicaciones).forEach(dpto => {
            selectDpto.innerHTML += `<option value="${dpto}">${dpto.replace(/_/g, ' ')}</option>`;
        });
    } catch (error) {
        console.error("Error cargando ubicaciones:", error);
        alert("No se pudieron cargar las ubicaciones dinámicas. Verifica tu Backend.");
    }
});

document.getElementById('dpto').addEventListener('change', (e) => {
    const dptoSeleccionado = e.target.value;
    const selectProv = document.getElementById('prov');
    const selectDist = document.getElementById('dist');
    
    selectProv.innerHTML = '<option value="">-- Seleccione Provincia --</option>';
    selectDist.innerHTML = '<option value="">-- Selecciona una provincia primero --</option>';
    selectDist.disabled = true;

    if (dptoSeleccionado && jerarquiaUbicaciones[dptoSeleccionado]) {
        selectProv.disabled = false;
        Object.keys(jerarquiaUbicaciones[dptoSeleccionado]).forEach(prov => {
            selectProv.innerHTML += `<option value="${prov}">${prov.replace(/_/g, ' ')}</option>`;
        });
    } else {
        selectProv.disabled = true;
    }
});

document.getElementById('prov').addEventListener('change', (e) => {
    const dptoSeleccionado = document.getElementById('dpto').value;
    const provSeleccionada = e.target.value;
    const selectDist = document.getElementById('dist');
    
    selectDist.innerHTML = '<option value="">-- Seleccione Distrito --</option>';

    if (provSeleccionada && jerarquiaUbicaciones[dptoSeleccionado]?.[provSeleccionada]) {
        selectDist.disabled = false;
        jerarquiaUbicaciones[dptoSeleccionado][provSeleccionada].forEach(dist => {
            selectDist.innerHTML += `<option value="${dist}">${dist.replace(/_/g, ' ')}</option>`;
        });
    } else {
        selectDist.disabled = true;
    }
});

// =========================================================================
// PARTE 2: CONSULTA A LA IA (CLICK EN EL BOTÓN)
// =========================================================================

document.getElementById('formulario-agro').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const dpto = document.getElementById('dpto').value;
    const prov = document.getElementById('prov').value;
    const dist = document.getElementById('dist').value;

    if (!dpto || !prov || !dist) {
        alert("Por favor selecciona un Departamento, Provincia y Distrito.");
        return;
    }

    document.getElementById('cargando').classList.remove('hidden');
    document.getElementById('resultados').classList.add('hidden');

    try {
        // ==========================================
        // PASO 1: PEDIR OPORTUNIDADES DEL MES ACTUAL Y SU FICHA
        // ==========================================
        const resTemporada = await fetch(`${baseUrl}/temporada/oportunidades?dpto=${dpto}&prov=${prov}&dist=${dist}`);
        const dataTemporada = await resTemporada.json();

        document.getElementById('nombre-mes-actual').innerText = dataTemporada.mes_nombre;
        const contenedorTemporada = document.getElementById('lista-temporada');
        contenedorTemporada.innerHTML = '';

        dataTemporada.oportunidades.forEach((item, idx) => {
            contenedorTemporada.innerHTML += `
                <div class="flex justify-between items-center bg-white/20 border border-white/30 p-3 rounded-xl text-sm shadow-sm">
                    <div>
                        <span class="font-bold block text-lg">${idx + 1}. ${item.cultivo.replace(/_/g, ' ')}</span>
                        <span class="text-xs text-amber-100">Si siembras ahora, rendirá: ${item.rendimiento_promedio.toLocaleString()} kilos por hectárea</span>
                    </div>
                    <div class="text-right">
                        <span class="font-black block text-xl">S/ ${item.precio_promedio}</span>
                        <span class="text-[10px] text-amber-200 font-medium uppercase tracking-wider">por kilo</span>
                    </div>
                </div>
            `;
        });

        // Buscamos la guía de cuidados para el ganador de ESTE MES (Opción 1 de la caja naranja)
        if (dataTemporada.oportunidades.length > 0) {
            const cultivoMesGanador = dataTemporada.oportunidades[0].cultivo;
            const resFichaMes = await fetch(`${baseUrl}/agronomia/ficha?cultivo=${cultivoMesGanador}`);
            const dataFichaMes = await resFichaMes.json();

            document.getElementById('ficha-titulo-mes').innerText = cultivoMesGanador.replace(/_/g, ' ');
            document.getElementById('ficha-temp-mes').innerText = dataFichaMes.temp_ideal;
            document.getElementById('ficha-agua-mes').innerText = dataFichaMes.agua_minima;
            document.getElementById('ficha-suelo-mes').innerText = dataFichaMes.suelo;
            document.getElementById('ficha-tip-mes').innerText = dataFichaMes.tip_cuidado;

            // Mostramos la cajita
            document.getElementById('ficha-mes-container').classList.remove('hidden');
        }

        // ==========================================
        // PASO 2: PEDIR LA RECOMENDACIÓN DE LA IA (TOP 3 GENERAL)
        // ==========================================
        const resCultivos = await fetch(`${baseUrl}/cultivos/recomendar?dpto=${dpto}&prov=${prov}&dist=${dist}`);
        const dataCultivos = await resCultivos.json();

        const contenedorTop3 = document.getElementById('lista-top3');
        contenedorTop3.innerHTML = ''; 

        const top3Nombres = [];

        dataCultivos.data.recomendaciones.forEach((item, index) => {
            top3Nombres.push(item.cultivo); 
            
            const esTop1 = index === 0;
            const bgClass = esTop1 ? 'bg-white/30 border-white/50 shadow-md' : 'bg-white/10 border-white/20';
            const icon = esTop1 ? '🏆' : (index === 1 ? '🥈' : '🥉');
            const probNumber = parseFloat(item.probabilidad_exito);
            
            let mensajeIntuitivo = probNumber >= 50 ? "🌱 Tu tierra es perfecta para este cultivo" : (probNumber >= 15 ? "💧 Va a crecer bien, pero cuídalo mucho" : "⚠️ Es riesgoso sembrar esto en tu terreno");

            contenedorTop3.innerHTML += `
                <div class="flex flex-col p-3 md:p-4 rounded-xl border ${bgClass}">
                    <div class="flex justify-between items-center mb-2">
                        <div class="flex items-center">
                            <span class="text-2xl mr-3">${icon}</span>
                            <div>
                                <span class="${esTop1 ? 'font-bold text-xl' : 'font-semibold text-lg'} block leading-tight">${item.cultivo.replace(/_/g, ' ')}</span>
                                <span class="text-xs text-green-100 opacity-90">${mensajeIntuitivo}</span>
                            </div>
                        </div>
                        <div class="text-white font-black text-lg">${item.probabilidad_exito}</div>
                    </div>
                    <div class="w-full bg-green-900/30 rounded-full h-2 mt-1">
                        <div class="bg-white h-2 rounded-full transition-all duration-1000 ease-out" style="width: ${probNumber}%"></div>
                    </div>
                </div>
            `;
        });

        const cultivoGanador = top3Nombres[0]; 

        // ==========================================
        //  PASO 3: CALENDARIO DE SIEMBRA
        // ==========================================
        const contenedorCalendario = document.getElementById('lista-calendario');
        contenedorCalendario.innerHTML = '<p class="text-xs text-gray-500 mb-3 italic">Para tener una buena cosecha, guarda la semilla y métela a la tierra solo en estos meses:</p>';

        const promesasCalendario = top3Nombres.map(nombreCultivo => 
            fetch(`${baseUrl}/calendario/optimo?dpto=${dpto}&prov=${prov}&dist=${dist}&cultivo=${nombreCultivo}`).then(res => res.json())
        );
        
        const resultadosCalendarios = await Promise.all(promesasCalendario);

        resultadosCalendarios.forEach((dataCal, index) => {
            const nombreLimpio = top3Nombres[index].replace(/_/g, ' ');
            const iconoList = ['🏆', '🥈', '🥉'];
            
            let htmlMeses = dataCal.mejores_meses.map(mes => 
                `<span class="bg-green-100 border border-green-200 text-green-800 px-3 py-1 rounded-lg text-xs font-bold inline-block mb-1 mr-1">${mes.mes_nombre}</span>`
            ).join('');

            contenedorCalendario.innerHTML += `
                <div class="bg-gray-50 border border-gray-100 p-3 rounded-xl">
                    <p class="text-sm font-bold text-gray-700 mb-2">${iconoList[index]} Si vas a sembrar ${nombreLimpio}, hazlo en:</p>
                    <div class="flex flex-wrap">
                        ${htmlMeses || '<span class="text-xs text-gray-400">No hay datos suficientes</span>'}
                    </div>
                </div>
            `;
        });

        // ==========================================
        // PASO 4: ALERTAS CLIMÁTICAS
        // ==========================================
        const resAlertas = await fetch(`${baseUrl}/alertas/evaluar?dpto=${dpto}&prov=${prov}&dist=${dist}`);
        const dataAlertas = await resAlertas.json();
        const contenedorAlertas = document.getElementById('lista-alertas');
        
        contenedorAlertas.innerHTML = `<p class="text-xs text-gray-500 mb-3 italic">Según el clima normal de tu zona, ten mucho cuidado con lo siguiente si vas a sembrar ${cultivoGanador.replace(/_/g, ' ')}:</p>`;

        if (dataAlertas.alertas.length === 0) {
            contenedorAlertas.innerHTML += `<div class="p-3 rounded-lg text-sm bg-green-50 text-green-700 border border-green-200">✅ Tu zona tiene un clima excelente, no hay alertas graves.</div>`;
        } else {
            dataAlertas.alertas.forEach(alerta => {
                let colorClass = alerta.nivel.includes('ROJO') ? 'bg-red-100 text-red-800 border-red-200' : (alerta.nivel.includes('AMARILLO') ? 'bg-yellow-100 text-yellow-800 border-yellow-200' : 'bg-green-100 text-green-800 border-green-200');
                let nivelAmigable = alerta.nivel.includes('ROJO') ? '⚠️ MUCHO CUIDADO' : (alerta.nivel.includes('AMARILLO') ? '👀 PRECAUCIÓN' : '✅ TODO BIEN');

                contenedorAlertas.innerHTML += `<div class="p-2.5 rounded-lg text-xs border shadow-sm mb-2 ${colorClass}"><strong>${nivelAmigable}:</strong> ${alerta.mensaje}</div>`;
            });
        }

        // ==========================================
        // PASO 5: TENDENCIA DE PRECIOS
        // ==========================================
        const resPrecios = await fetch(`${baseUrl}/precios/tendencia?dpto=${dpto}&prov=${prov}&dist=${dist}&cultivo=${cultivoGanador}`);
        const dataPrecios = await resPrecios.json();
        const dataEcon = dataPrecios.datos_economicos;
        
        document.getElementById('res-precio').innerHTML = `S/ ${dataEcon.precio_mas_reciente} <span class="text-sm font-normal text-gray-500 block">por kilo (aprox)</span>`;
        
        let tendenciaElement = document.getElementById('res-tendencia');
        
        if (dataEcon.tendencia_general.includes('ALZA')) {
            tendenciaElement.innerHTML = `¡Está subiendo! 📈<span class="text-xs font-normal block text-green-700 mt-1">Buen momento para vender</span>`;
            tendenciaElement.className = "text-md font-bold text-green-600";
        } else if (dataEcon.tendencia_general.includes('BAJA')) {
            tendenciaElement.innerHTML = `Está bajando 📉<span class="text-xs font-normal block text-red-700 mt-1">Cuidado con las ganancias</span>`;
            tendenciaElement.className = "text-md font-bold text-red-600";
        } else {
            tendenciaElement.innerHTML = `Se mantiene estable ➖<span class="text-xs font-normal block text-gray-500 mt-1">Precio normal de mercado</span>`;
            tendenciaElement.className = "text-md font-bold text-gray-600";
        }

        // ==========================================
        // PASO 6: FICHA TÉCNICA DEL CULTIVO GENERAL (El ganador de la IA)
        // ==========================================
        const resFichaGen = await fetch(`${baseUrl}/agronomia/ficha?cultivo=${cultivoGanador}`);
        const dataFichaGen = await resFichaGen.json();

        document.getElementById('ficha-titulo').innerText = cultivoGanador.replace(/_/g, ' ');
        document.getElementById('ficha-temp').innerText = dataFichaGen.temp_ideal;
        document.getElementById('ficha-agua').innerText = dataFichaGen.agua_minima;
        document.getElementById('ficha-suelo').innerText = dataFichaGen.suelo;
        document.getElementById('ficha-tip').innerText = dataFichaGen.tip_cuidado;

        // Ocultar spinner
        document.getElementById('cargando').classList.add('hidden');
        document.getElementById('resultados').classList.remove('hidden');
        
    } catch (error) {
        console.error("Error en la API:", error);
        document.getElementById('cargando').classList.add('hidden');
        alert("¡Oops! No pudimos conectar con los motores de Inteligencia Artificial. Revisa que tu servidor de FastAPI esté corriendo.");
    }
});