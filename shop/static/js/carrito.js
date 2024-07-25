<script type="text/javascript">
    console.log('prueba');
    let cesta;

    if (localStorage.getItem('cesta') !== null) {
        cesta = JSON.parse(localStorage.getItem('cesta')); 
    } else {
        cesta = {}; 
    }

    $(document).on('click', '.ted', function() {
        console.log('agregar');
        var item_id = this.id.toString();
        console.log(item_id);
        if (cesta[item_id] !== undefined) {
            cesta[item_id] = cesta[item_id] + 1;
        } else {
            cesta[item_id] = 1;
        }
        console.log(cesta);
        localStorage.setItem('cesta', JSON.stringify(cesta));
        document.getElementById("cesta").innerHTML = "Cesta(" + Object.keys(cesta).length + ")";
    });

  
    MostrarLista(cesta);
    function MostrarLista(cesta){
    var cestaString = "";
    cestaString += "<h5>Lista</h5>";
    var tienda =1;
    for(var x in cesta){
        cestaString += tienda;
        cestaString += document.getElementById("aa" +x).innerHTML +"Qte"+ cesta[x]
        tienda +=1;
    }
    $('[data-toggle="popover"]').popover();
        document.getElementById('cesta').setAttribute('data-content', cestaString);
        
      
</script>
{% endblock %}