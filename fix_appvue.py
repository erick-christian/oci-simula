import sys

path = "/var/www/oci-app/frontend/src/App.vue"
with open(path, "r") as f:
    content = f.read()

# Fix 1: Add the closing tags for the 'inicio' screen and the opening tag for 'jugando' which I deleted.
search_str1 = """          <button @click="comenzarExamen" :disabled="cargando"
            class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 flex justify-center items-center text-lg disabled:opacity-70 disabled:cursor-not-allowed">
        <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-2xl shadow-sm border">"""

replace_str1 = """          <button @click="comenzarExamen" :disabled="cargando"
            class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 flex justify-center items-center text-lg disabled:opacity-70 disabled:cursor-not-allowed">
            Comenzar
          </button>
        </div>
      </div>

      <div v-else-if="pantalla === 'jugando'" class="min-h-screen flex flex-col bg-gray-50">
        <header class="bg-white shadow-sm sticky top-0 z-40 px-2 py-2 md:px-6 md:py-3 flex justify-between items-center border-b border-gray-100">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 md:w-10 md:h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold shadow-inner flex-shrink-0">
              {{ getIniciales() }}
            </div>
            <div class="hidden sm:block">
              <p class="text-xs text-gray-500 font-medium">Alumno</p>
              <p class="font-bold text-gray-800 leading-tight truncate max-w-[120px] md:max-w-xs">{{ nombreEstudiante }} {{ apellidoEstudiante }}</p>
            </div>
          </div>
          
          <div class="flex items-center gap-2 md:gap-4">
            <button @click="solicitarMasTiempo" 
              class="flex items-center gap-1 md:gap-2 px-2 py-1.5 md:px-3 md:py-2 text-xs md:text-sm font-medium text-amber-700 bg-amber-50 hover:bg-amber-100 rounded-lg transition-colors border border-amber-200">
              <svg class="w-3.5 h-3.5 md:w-4 md:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span class="hidden md:inline">+5 Minutos</span><span class="md:hidden">+5m</span>
              <span v-if="vecesTiempoSolicitado > 0" class="ml-1 bg-amber-200 text-amber-800 py-0.5 px-1.5 rounded-full text-[10px] leading-none">{{vecesTiempoSolicitado}}</span>
            </button>

            <div class="flex items-center gap-1.5 bg-gray-50 px-2 py-1.5 md:px-4 md:py-2 rounded-lg border border-gray-200 shadow-inner" :class="{'text-red-600 bg-red-50 border-red-200 animate-pulse': tiempoRestante < 300}">
              <svg class="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span class="font-mono font-bold text-sm md:text-lg tracking-wider">{{ tiempoFormateado }}</span>
            </div>
          </div>
        </header>
        <main class="flex-grow w-full md:max-w-4xl max-w-full mx-auto p-2 sm:p-4 flex flex-col">
          <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-2xl shadow-sm border">"""

if search_str1 in content:
    content = content.replace(search_str1, replace_str1)
    print("Fix 1 applied successfully.")
else:
    print("Fix 1 target not found.")

# Fix 2: Remove the bogus mobile header that was wrongfully injected into the admin section around line 827.
search_str2 = """      <div v-else-if="pantalla === 'admin'"
        class="w-full bg-white rounded-3xl shadow-xl overflow-hidden max-w-7xl mx-auto flex flex-col h-[90vh]">
     <div v-if="pantalla === 'jugando'" class="min-h-screen flex flex-col bg-gray-50">
      <!-- Modified: header reducido para optimización móvil -->
      <header class="bg-white shadow-sm sticky top-0 z-40 px-2 py-2 md:px-6 md:py-3 flex justify-between items-center border-b border-gray-100">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 md:w-10 md:h-10 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold shadow-inner flex-shrink-0">
            {{ getIniciales() }}
          </div>
          <div class="hidden sm:block">
            <p class="text-xs text-gray-500 font-medium">Alumno</p>
            <p class="font-bold text-gray-800 leading-tight truncate max-w-[120px] md:max-w-xs">{{ nombreEstudiante }} {{ apellidoEstudiante }}</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2 md:gap-4">
          <!-- Boton de Solicitar Tiempo Extra (Optimizado móvil) -->
          <button @click="solicitarMasTiempo" 
            class="flex items-center gap-1 md:gap-2 px-2 py-1.5 md:px-3 md:py-2 text-xs md:text-sm font-medium text-amber-700 bg-amber-50 hover:bg-amber-100 rounded-lg transition-colors border border-amber-200">
            <svg class="w-3.5 h-3.5 md:w-4 md:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span class="hidden md:inline">+5 Minutos</span><span class="md:hidden">+5m</span>
            <span v-if="vecesTiempoSolicitado > 0" class="ml-1 bg-amber-200 text-amber-800 py-0.5 px-1.5 rounded-full text-[10px] leading-none">{{vecesTiempoSolicitado}}</span>
          </button>

          <!-- Timer optimizado móvil -->
          <div class="flex items-center gap-1.5 bg-gray-50 px-2 py-1.5 md:px-4 md:py-2 rounded-lg border border-gray-200 shadow-inner" :class="{'text-red-600 bg-red-50 border-red-200 animate-pulse': tiempoRestante < 300}">
            <svg class="w-4 h-4 md:w-5 md:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span class="font-mono font-bold text-sm md:text-lg tracking-wider">{{ tiempoFormateado }}</span>
          </div>
        </div>
      </header>
      
      <!-- Modified: main content sin padding vertical excesivo para no empujar la tarjeta hacia abajo -->
      <main class="flex-grow w-full md:max-w-4xl max-w-full mx-auto p-2 sm:p-4 flex flex-col">ass="text-gray-500 hover:text-indigo-600 font-bold bg-gray-50 px-4 py-2 rounded-xl">Cerrar</button>
        </div>"""

replace_str2 = """      <div v-else-if="pantalla === 'admin'"
        class="w-full bg-white rounded-3xl shadow-xl overflow-hidden max-w-7xl mx-auto flex flex-col h-[90vh]">
        <!-- Cabecera Sticky -->
        <div class="p-6 border-b bg-white sticky top-0 z-20 flex justify-between items-center shrink-0">
          <div class="flex items-center gap-6">
            <h2 class="text-2xl font-bold text-slate-800">Panel de Control</h2>
            <div class="flex bg-gray-100 p-1 rounded-xl">
              <button @click="vistaAdmin = 'resultados'" class="px-4 py-2 rounded-lg font-bold text-sm transition"
                :class="vistaAdmin === 'resultados' ? 'bg-white shadow text-indigo-700' : 'text-gray-500 hover:text-gray-700'">
                📊 Resultados Generales
              </button>
              <button @click="vistaAdmin = 'reportadas'"
                class="px-4 py-2 rounded-lg font-bold text-sm transition flex items-center gap-2"
                :class="vistaAdmin === 'reportadas' ? 'bg-white shadow text-indigo-700' : 'text-gray-500 hover:text-gray-700'">
                🚩 Preguntas Reportadas
                <span v-if="preguntasReportadas.length > 0"
                  class="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">{{ preguntasReportadas.length }}</span>
              </button>
              <button @click="vistaAdmin = 'rendimiento'" class="px-4 py-2 rounded-lg font-bold text-sm transition"
                :class="vistaAdmin === 'rendimiento' ? 'bg-white shadow text-indigo-700' : 'text-gray-500 hover:text-gray-700'">
                📈 Rendimiento Alumno
              </button>
            </div>
          </div>
          <button @click="pantalla = 'inicio'"
            class="text-gray-500 hover:text-indigo-600 font-bold bg-gray-50 px-4 py-2 rounded-xl">Cerrar</button>
        </div>"""

if search_str2 in content:
    content = content.replace(search_str2, replace_str2)
    print("Fix 2 applied successfully.")
else:
    print("Fix 2 target not found.")

# Missing closing tags for `<main>` inside the `pantalla === 'jugando'` wrapper block
search_str3 = """        <!-- PANEL PENDIENTES -->
        <div v-if="mostrarPanelPendientes"
          class="fixed inset-0 bg-slate-900/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm">"""

replace_str3 = """        </main>
      </div>

        <!-- PANEL PENDIENTES -->
        <div v-if="mostrarPanelPendientes"
          class="fixed inset-0 bg-slate-900/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm">"""

if search_str3 in content:
    content = content.replace(search_str3, replace_str3)
    print("Fix 3 applied successfully.")
else:
    print("Fix 3 target not found.")


with open(path, "w") as f:
    f.write(content)
print("File updated.")
