$(document).ready(function () {
  $("#checkbox-toggle-all").on("change", function () {
    $(".timesheet-checkbox").prop("checked", $(this).is(":checked")).trigger("change");
  });

  $(".timesheet-checkbox").on("change", function () {
    setupTimesheetData();
  });

  $("#btn-assign-project").on("click", function () {
    setupTimesheetData();
    var $form = $("#form-assign-project");
    var data = $form.serializeArray().reduce(function (object, item) {
      object[item.name] = item.value;
      return object;
    }, {});
    var errors = [];
    if (!data.project) {
      errors.push("Select a project to continue");
    }
    if (!data.timesheets) {
      errors.push("Select at least 1 timesheet");
    }
    if (errors.length) {
      alert(errors.join("\n"));
      return;
    }
    $("#form-assign-project").submit();
  });

  function setupTimesheetData () {
    var ids = [];
    $(".timesheet-checkbox:checked").each(function (index, checkbox) {
      ids.push($(checkbox).data("timesheet-id"));
    });
    $("#timesheets-quantity").text(ids.length);
    $("#id_timesheets").val(ids.join(","));
  }
});
