document.addEventListener("DOMContentLoaded", function () {
    const selectTransport = document.getElementById('select-transport');
    const addTransportBtn = document.getElementById('new_transport');
    const selectStart = document.getElementById('select-start');
    const addStartBtn = document.getElementById('new_start');
    const selectEnd = document.getElementById('select-end');
    const addEndBtn = document.getElementById('new_end');
    
    const selections = [selectTransport, selectStart, selectEnd]
    const addNewBtns = [addTransportBtn, addStartBtn, addEndBtn]
    selections.forEach((selection, index) => {
        selection.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
            if (selectedValue == 'new') {
                addNewBtns[index].style.display = 'block';
            }
        });
    })

    addNewBtns.forEach((btn, index) => {
        btn.addEventListener('input', (event) => {
            const newValue = event.target.value;
            selections[index].lastElementChild.value = newValue;
        })
    })
});