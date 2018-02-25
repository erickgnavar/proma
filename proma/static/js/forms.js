function setupFormset(parent, empty, relationName, addBtn) {
  var $parent = $(parent);
  var $empty = $(empty);
  var $totalFormset = $('#id_#name-TOTAL_FORMS'.replace('#name', relationName));

  $(addBtn).on('click', function () {
    var counter = parseInt($totalFormset.val());
    var compiled = $empty.html().replace(/__prefix__/g, counter);
    var node = $(compiled);
    $parent.append(node);
    $totalFormset.val(counter + 1);
  });
}
