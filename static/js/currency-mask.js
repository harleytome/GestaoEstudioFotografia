document.addEventListener('DOMContentLoaded', function () {
    var currencyInputs = document.querySelectorAll('.currency-mask');
    currencyInputs.forEach(function (input) {
        input.addEventListener('input', function (e) {
            var value = e.target.value.replace(/\D/g, '');
            if (value.length === 0) {
                e.target.value = '';
                return;
            }
            value = parseInt(value) / 100;
            e.target.value = value.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL',
            });
        });
        input.addEventListener('focus', function () {
            if (this.value === '') {
                this.value = 'R$ 0,00';
            }
            this.select();
        });
        input.addEventListener('blur', function () {
            if (this.value === 'R$ 0,00') {
                this.value = '';
            }
        });
    });
});
