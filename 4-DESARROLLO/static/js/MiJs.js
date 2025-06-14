
    function getFecha(){
        const d = new Date();
        let text = d.toString();
        return text;
    }

    function Ir(cual){
        document.forms['mio'].action="/niveles/"+cual
        document.forms['mio'].submit();
       }
       function IrF(cual){
        document.forms['mio'].action=cual
        document.forms['mio'].submit();
       }
       function Irc(formula,cual,que){
        document.forms[formula].action=cual+"/"+que.value;
        document.forms[formula].submit();
       }
       function Ir1(cual){
        location.href=cual
       }
        function Confirmar(que,donde){
            if (confirm(que)){
                //alert(donde);
                //location.href=donde;
                IrF(donde);

            }
              
        }
       function Va(tipo){
        
        if(tipo=="i")
        document.forms['mio'].action="/niveles/i"
        if(tipo=="u"){
         
         document.forms['mio'].action="/niveles/u"   
        }
        
        document.forms['mio'].submit();    
     
       }

       const searchInput = document.getElementById('search-input');
    const contentList = document.getElementById('content');

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const listItems = contentList.getElementsByTagName('li');

        for (let i = 0; i < listItems.length; i++) {
            const listItem = listItems[i];
            const listItemText = listItem.textContent.toLowerCase();

            if (listItemText.includes(searchTerm)) {
                listItem.style.display = ''; // Mostrar
            } else {
                listItem.style.display = 'none'; // Ocultar
            }
        }
    });
