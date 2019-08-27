$(document).ready(() => {
    console.log('help')
 $('[data-toggle="tooltip"]').tooltip()

 $('body > :not(#formid)').hide();
 //$('#topid').appendTo('body');
 $('#topid').show();
 $('[id=alwayson]').show();
 //$('#formid').appendTo('#topid');
 $("#formIDbutton").click(function()
 {
   $('body >').toggle();
   $('[id=neverhidden]').show();
   $("[id=keywordid]").hide();
   $("[id=barid]").hide();
    $('#topid').show();
   $('[id=alwayson]').show();
   $('#formid').hide();


 });

  $("#thumbnailIDbutton").click(function()
  {
    $("[id=keywordid]").show();
    $("[id=thumbnailid]").hide();
});

$("#keywordIDbutton").click(function()
{
  $("[id=keywordid]").hide();
  $("[id=barid]").show();
  });
  $("#barIDbutton").click(function()
  {
    $('*').show();
    $("#formIDbutton").hide()
    $("#thumbnailIDbutton").hide()
    $("#keywordIDbutton").hide()
    $("#barIDbutton").hide()
    });

});
