
// prevent users from inserting anything other than a number in the puzzle
$('[contenteditable="true"]').keypress(function(e) {
    var x = e.charCode || e.keyCode;
    if (x < 48 || x > 57 )
        e.preventDefault();
});



document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function() {
    
        document.getElementById('info').innerHTML = "";
        var inputPuzzle = document.getElementById('inputPuzzle');

        puzzleArray = new Array()
        for (let row of inputPuzzle.rows) 
        {
            line = []
            for(let cell of row.cells) 
            {   
                data = cell.innerText
                if (data == ''){
                    data = 0
                }
                else {
                    data = parseInt(data)
                }
                line.push(data)  
            }
            puzzleArray.push(line)
            
        }
        // ALLORA check on the website she calls some element info, so you can steal the html from it!!!
        

        $.ajax({
            type: "POST", 
            url: "http://127.0.0.1:5000/stage", //localhost Flask
            data : JSON.stringify(puzzleArray),
            contentType: "application/json",
        });
        
        return;
    };
});

