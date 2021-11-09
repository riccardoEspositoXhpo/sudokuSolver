
// prevent users from inserting anything other than a number in the puzzle
$('[contenteditable="true"]').keypress(function(e) {
    var x = e.charCode || e.keyCode;
    if (x < 48 || x > 57 )
        e.preventDefault();
});


document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function(e) {
    
        // make sure page is reloaded to capture any user changes
        location.reload();
        var inputPuzzle = document.getElementById('inputPuzzle');

        puzzleArray = new Array()

        // grab all the cells in the puzzle and fill in gaps with 0
        for (let row of inputPuzzle.rows) 
        {
            line = []
            for(let cell of row.cells) 
            {   
                data = cell.innerText
                if (data == '' || data == 'None'){
                    data = 0
                }
                else {
                    data = parseInt(data)
                }
                line.push(data)  
            }
            puzzleArray.push(line)
            
        }      

        // post request to flask with required data
        $.ajax({
            type: 'POST',
            url: '/stage',
            data: JSON.stringify(puzzleArray),
            success: function(data) { alert('data: ' + data); },
            contentType: "application/json",
            dataType: 'json'
        });
        
        return;
    };
});

