// gerenciador_app/frontEnd/static/js/dashboard.js

document.addEventListener('alpine:init', () => {
    Alpine.data('financeApp', (initialData) => ({
        showGastoForm: false, showEntradaForm: false,
        editGastoModal: false, editEntradaModal: false,
        editGastoData: {}, editEntradaData: {},
        total_entradas: initialData.total_entradas,
        total_gastos: initialData.total_gastos,
        saldo: initialData.saldo,
        snoopy_imagem: initialData.snoopy_imagem,
        snoopy_texto: '', snoopy_cor: '',

        // --- NOVOS ESTADOS PARA OS GRÁFICOS UNIFICADOS ---
        showCharts: false,       // Controla a visibilidade da área toda
        chartCategory: null,     // Instância do gráfico de categorias
        chartBank: null,         // Instância do gráfico de bancos
        chartError: '',

        init() { this.updateSnoopy(); },

        updateRowStyle(element) {
            const row = element.closest('tr');
            if (element.checked) { row.classList.add('text-gray-400', 'line-through', 'opacity-70'); } 
            else { row.classList.remove('text-gray-400', 'line-through', 'opacity-70'); }
        },
        updateSnoopy() {
            if (this.saldo <= 0 && this.total_gastos > 0) {
                this.snoopy_imagem = '/static/images/snoopy_triste.gif';
                this.snoopy_texto = 'Cuidado com os gastos!'; this.snoopy_cor = 'text-red-600';
            } else if (this.saldo > (this.total_entradas * 0.7) && this.total_entradas > 0) {
                this.snoopy_imagem = '/static/images/snoopy_feliz.gif';
                this.snoopy_texto = 'Você está indo ótimo!'; this.snoopy_cor = 'text-green-600';
            } else {
                this.snoopy_imagem = '/static/images/snoopy_normal.gif';
                this.snoopy_texto = 'Tudo sob controle.'; this.snoopy_cor = 'text-snoopy-blue';
            }
        },
        async toggleGasto(id, valor, element) {
            this.updateRowStyle(element);
            if (element.checked) { this.total_gastos += valor; this.saldo -= valor; } 
            else { this.total_gastos -= valor; this.saldo += valor; }
            this.updateSnoopy();
            await fetch(`/toggle_gasto/${id}`, { method: 'POST' });
        },
        async toggleEntrada(id, valor, element) {
            this.updateRowStyle(element);
            if (element.checked) { this.total_entradas += valor; this.saldo += valor; } 
            else { this.total_entradas -= valor; this.saldo -= valor; }
            this.updateSnoopy();
            await fetch(`/toggle_entrada/${id}`, { method: 'POST' });
        },
        async deleteGasto(id, valor, isChecked, element) {
            if (!confirm('Tem certeza?')) return;
            element.closest('tr').remove();
            if (isChecked) { this.total_gastos -= valor; this.saldo += valor; this.updateSnoopy(); }
            await fetch(`/delete_gasto/${id}`, { method: 'POST' });
        },
        async deleteEntrada(id, valor, isChecked, element) {
            if (!confirm('Tem certeza?')) return;
            element.closest('tr').remove();
            if (isChecked) { this.total_entradas -= valor; this.saldo -= valor; this.updateSnoopy(); }
            await fetch(`/delete_entrada/${id}`, { method: 'POST' });
        },
        async openEditGasto(id) { const r = await fetch(`/api/get_gasto/${id}`); if (r.ok) { this.editGastoData = await r.json(); this.editGastoModal = true; } },
        async openEditEntrada(id) { const r = await fetch(`/api/get_entrada/${id}`); if (r.ok) { this.editEntradaData = await r.json(); this.editEntradaModal = true; } },

        // --- FUNÇÃO UNIFICADA DE GRÁFICOS ---
        async toggleCharts() {
            this.chartError = '';
            this.showCharts = !this.showCharts;

            // Se estiver fechando, destrói ambos os gráficos para limpar memória
            if (!this.showCharts) {
                if (this.chartCategory) { this.chartCategory.destroy(); this.chartCategory = null; }
                if (this.chartBank) { this.chartBank.destroy(); this.chartBank = null; }
                return;
            }

            // Se já existirem (por algum clique rápido), destrói antes de recriar
            if (this.chartCategory) this.chartCategory.destroy();
            if (this.chartBank) this.chartBank.destroy();

            // Chama as duas funções de renderização em paralelo
            this.renderCategoryChart();
            this.renderBankChart();
        },

        async renderCategoryChart() {
            try {
                const res = await fetch('/api/gastos_por_categoria');
                const data = await res.json();
                if (data.labels.length === 0 && !this.chartError) { // Só mostra erro se for o primeiro a falhar
                     this.chartError = 'Sem dados de gastos pagos para os gráficos.';
                     // Não fechamos this.showCharts aqui para deixar o outro gráfico tentar carregar
                     return;
                }
                const ctx = document.getElementById('categoryChart').getContext('2d');
                this.chartCategory = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: ['#EF4444', '#3B82F6', '#FACC15', '#10B981', '#6366F1', '#8B5CF6'],
                            hoverOffset: 4
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
                });
            } catch (e) { console.error(e); if(!this.chartError) this.chartError = 'Erro ao carregar gráfico de categorias.'; }
        },

        async renderBankChart() {
            try {
                const res = await fetch('/api/gastos_por_banco');
                const data = await res.json();
                if (data.labels.length === 0) return; // Se não tem dados, só não renderiza, sem erro extra
                
                const ctx = document.getElementById('bankChart').getContext('2d');
                this.chartBank = new Chart(ctx, {
                    type: 'doughnut', // ou 'pie'
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            // Cores diferentes para o gráfico de bancos
                            backgroundColor: ['#8B5CF6', '#EC4899', '#14B8A6', '#F59E0B', '#64748B', '#0EA5E9'],
                            hoverOffset: 4
                        }]
                    },
                    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
                });
            } catch (e) { console.error(e); }
        }
    }));
});