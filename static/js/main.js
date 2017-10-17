/**
 MIT License

 Copyright (c) 2017 Franco Cavestri

 https://github.com/cavestri/feedback

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 */


$(document).ready(function() {

    $('#loading')
        .hide()
        .ajaxStart(function() {
            $(this).show();
        })
        .ajaxStop(function() {
            $(this).hide();
        });

    loadData('get');

    $('#submit-filter').click(function () {
        var range = $('#range').val();
        var type = $('#type').val();
        if(range == 'all' && type == 'all') {
            loadData('get');
        } else if(range == 'all' && type != 'all'){
            loadData('get?type=' + type);
        } else if(type == 'all' && range != 'all'){
            loadData('get?range=' + range)
        } else {
            loadData('get?range=' + range + '&type=' + type)
        }
    });
});

function loadData(url) {
    var tableBody = $('#feedback_table tbody');
    tableBody.empty();
    tableBody.append('<td colspan="4">Loading...</td>');
    $.ajax(url)
        .done(function (response) {
            tableBody.empty();

            var issues = $.grep(response, function (item) {
                return item['type'] == 'issue';
            });

            var likes = $.grep(response, function (item) {
                return item['type'] == 'like';
            });

            var dislikes = $.grep(response, function (item) {
                return item['type'] == 'dislike';
            });

            $('#bubbles li.like span:first-child').text(likes.length);
            $('#bubbles li.dislike span:first-child').text(dislikes.length);
            $('#bubbles li.issue span:first-child').text(issues.length);

            if(response.length == 0) {
                tableBody.append('<td colspan="4">There are no items to show...</td>');
            }
            response.forEach(function (element) {
                tableBody.append('<tr>' +
                    '<td><i class="icon-' + element['type'] +'"></i></td>' +
                    '<td> ' + element['user'] + ' </td>' +
                    '<td> ' + element['comment'] + ' </td>' +
                    '<td> ' + element['date'] + ' </td>' +
                    '</tr>');
            });
        })
        .fail(function(response) {
            console.log(response);
        });
}