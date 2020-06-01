$(function () {
    var board = $('#board')[0];
    var size = 19;
    var current = true;
    var currentColor = true;
    var over = false;

    board.init = function () {
        this.moves = [];
        over = false;
        current = !$('[name="choice"]')[0].checked;
        currentColor = !current;
        var playerIndex = current ? 1 : -1;
        this.draw();
        accessData('restart', {playerIndex: playerIndex}, function (data) {
            if (data.status == 'OK') {
                accessData('aiplay', null, function (data) {
                    if (data.status == 'OK') {
                        board.put(data.move.x, data.move.y, board.moves.length + 1, !currentColor);
                        current = !current;
                    }
                });
            }
        });
    };

    board.draw = function () {
        var desk = $(this).find('table.desk');
        var htmlString = '<tbody><tr><th></th>';
        var a = 'a'.charCodeAt(0);
        for (var j = 0; j < size; j++) {
            var ch = String.fromCharCode(a + j);
            htmlString += '<th>' + ch + '</th>';
        }
        htmlString += '<th></th></tr>';

        for (var i = 0; i < size; i++) {
            htmlString += '<tr data-row="' + i + '"><th>' + (size - i) + '</th>';
            for (var j = 0; j < size; j++) {
                htmlString += '<td class="freecell" data-col="' + j + '">&nbsp;</td>';
            }
            htmlString += '<th>' + (size - i) + '</th></tr>';
        }
        htmlString += '<tr><th></th>';

        for (var j = 0; j < size; j++) {
            var ch = String.fromCharCode(a + j);
            htmlString += '<th>' + ch + '</th>';
        }
        htmlString += '<th></th></tr></tbody>';
        desk.html(htmlString);
    };

    board.put = function (i, j, ch, current) {
        board.moves.push([i, j]);
        if (current) {
            var color = 'white';
        } else {
            var color = 'black';
        }
        var $td = $(this).find('table.desk > tbody > tr[data-row="' + i + '"] > td[data-col="' + j + '"]');
        if (ch) {
            $td.html(ch);
        }
        $td.removeClass('freecell').addClass(color);
    };

    board.init();

    $(board).on('click', 'table.desk > tbody > tr > td.freecell', function () {
        if (!current) return;
        if (over) return;
        $(this).removeClass('freecell').addClass(currentColor ? 'white' : 'black').html(board.moves.length + 1);
        var i = $(this).parent().data('row');
        var j = $(this).data('col');
        board.moves.push([i, j]);
        accessData('play', {x: i, y: j}, function (data) {
            over = data.game_status.finished;
            if (over) {
                alert('You won!');
                current = false;
            } else {
                current = !current;
                accessData('aiplay', null, function (data) {
                    if (data.status === 'OK') {
                        board.put(data.move.x, data.move.y, board.moves.length + 1, !currentColor);
                        over = data.game_status.finished;
                        if (over) {
                            alert('You lost');
                        } else {
                            current = !current;
                        }
                    }
                });
            }
        });
    });
    $(document).on('click', '[data-action]', function (event) {
        var action = $(this).data('action');
        if (board[action])
            board[action].call(board);
        event.preventDefault();
        event.stopPropagation();
    });
});
