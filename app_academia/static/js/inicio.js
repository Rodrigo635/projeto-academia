  document.addEventListener('DOMContentLoaded', function(){
    const btn = document.getElementById('btn-finalizar');
    const form = document.getElementById('form-principal');
    const modalEl = document.getElementById('modalSession');
    const modal = new bootstrap.Modal(modalEl);

    // Cancela o envio do form principal e abre o modal
    form.addEventListener('submit', function(e){
      e.preventDefault();
      modal.show();
    });
  });