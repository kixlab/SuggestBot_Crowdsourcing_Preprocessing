import boto3
from .models import *
from .MTURKKEY import *

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
TIME_FOR_EACH_PROMPT = 180
TIME_FOR_TUTORIAL = 300
HOURLY_PAYMENT =8
worker_requirements = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThan',
    'IntegerValues': [95],
    'ActionsGuarded': 'PreviewAndAccept',
},
{
    'QualificationTypeId': '00000000000000000071',
    'Comparator': 'In',
    'LocaleValues': [{
        'Country': 'US',
    }],
    'ActionsGuarded': 'PreviewAndAccept',
}]

html_question = """<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
  <HTMLContent><![CDATA[
<!DOCTYPE html>
<html>
<head></head>
<body>
<meta content="width=device-width,initial-scale=1" name="viewport" />
<section class="container" id="SurveyLink"><!-- Instructions -->
<div class="row">
<div class="col-xs-12 col-md-12">
<div class="panel panel-primary"><!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature --><a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>Labeling Task Link Instructions</strong> <span class="collapse-text">(Click to expand)</span> </a>
<div class="panel-body" id="instructionBody">
<p>In the task, you will label emotion and related phenomenons, like expressions and appraisal on the event, while watching a video. For it you will first be asked to walk through a test that helps you understand our answer criteria, and you will also read through a short tutorial to do the task. Then we will allow you to do the task, but <b>don’t worry: training times are included in the payment</b>.</p>
<p>
 Because we need to check whether your audio is on for this task, please click <b>‘Listen to the Sound’</b> button and dictate the word you heard in the text input next to <b>‘Enter the Sound Code’</b> button. When you dictated, hit <b>‘Enter the Sound Code’</b> button,  and the link will be given. Select the link below to complete the task. At the end of the task, you will receive a code to paste into the box below to receive credit for completing our task.</p>

<p><strong>Make sure to leave this window open as you complete the task. </strong> When you are finished, you will return to this page to paste the code into the box.</p>

<p><b>Please use Chrome for the task!!!!</b></p>

<p>If have any problems, contact johnr0hol@gmail.com, which will response faster.</p>
</div>
</div>
</div>
</div>
<!-- End Instructions --><!-- Survey Link Layout -->

<div class="row" id="workContent">
<div class="col-xs-12 col-md-6 col-md-offset-3"><!-- Content for Worker --></div>
</div>
<button onclick="play_text()" style="display:block; margin:auto;" type="button">Listen to the Sound</button>

<div style="display:block; margin-left:50%; position:relative; left:-140px;"><input id="sound_code" type="text" /><button onclick="code_confirm()">Enter the Sound Code</button></div>

<table class="table table-condensed table-bordered">
<colgroup>
<col class="col-xs-4 col-md-4" />
<col class="col-xs-8 col-md-8" />
</colgroup>
<tbody>
<tr>
<td><label>Task link:</label></td>
<td id="link_to_task">
<div id="myelementLink" style="display:none">a</div>
<span id="link_blocker">Input the sound code above to see the link.</span></td>
</tr>
</tbody>
</table>
<script
  src="https://code.jquery.com/jquery-3.3.1.slim.js"
  integrity="sha256-fNXJFIlca05BIO2Y5zh1xrShK3ME+/lYZ0j+ChxX2DA="
  crossorigin="anonymous"></script><script>
var keywords = ['dog', 'cat', 'lion', 'tiger', 'frog', 'elephant', 'giraffe', 'mule', 'horse', 'bear']
var key = Math.floor(Math.random()*keywords.length)
var voices = speechSynthesis.getVoices();
function play_text(){
  var message = new SpeechSynthesisUtterance(keywords[key])
  speechSynthesis.speak(message);
}
function code_confirm(){
  if(keywords[key] == $('#sound_code').val()){
    $("#link_blocker").css("display","none")
    $("#myelementLink").css("display","")
  }
}

var assignment_id_field = document.getElementById('myelementLink');
var paramstr = window.location.search.substring(1);
var parampairs = paramstr.split("&");
var mturkworkerID = "";
var assignmentID = "";
for (i in parampairs) {
 var pair = parampairs[i].split("=");
 if (pair[0] == "workerId"){
 mturkworkerID = pair[1];
 }else if(pair[0] == "assignmentId"){
 assignmentID = pair[1];
 }
}
if (mturkworkerID == "" && assignmentID == "" ) {
 assignment_id_field.innerHTML = '<tt>The link will appear here only if you accept this HIT.</tt>';
} else {
 assignment_id_field.innerHTML = '<a target="_blank" href="http://115.68.222.144:3000/emotion_labeling/_condition_/_video_title_/' + mturkworkerID + '/'+assignmentID+'"><h1><span style="color: rgb(255, 0, 0);"><span style="font-family: Courier New;"><b>Click here to begin taking the task!</b></span></span></h1></a>';
}
</script><!-- End Content for Worker --><!-- Input from Worker -->

<div class="form-group"><label for="surveycode">Provide the task code here:</label> <input class="form-control" id="surveycode" name="surveycode" placeholder="e.g. 12abcd56" required="" type="text" /></div>
<!-- End input from Worker --><!-- End Survey Link Layout --></section>
<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" />
<style type="text/css">#collapseTrigger{
  color:#fff;
  display: block;
  text-decoration: none;
}
#submitButton{
  white-space: normal;
}
.image{
  margin-bottom: 15px;
}
/* CSS for breaking long words/urls */
.dont-break-out {
  overflow-wrap: break-word;
  word-wrap: break-word;
  -ms-word-break: break-all;
  word-break: break-all;
  word-break: break-word;
  -ms-hyphens: auto;
  -moz-hyphens: auto;
  -webkit-hyphens: auto;
  hyphens: auto;
}
</style>
<p>
<style type="text/css">&nbsp;
</style>
</p>

<p>&nbsp;</p>

<p>&nbsp;</p>
</body>
</html>
]]>
  </HTMLContent>
  <FrameHeight>450</FrameHeight>
</HTMLQuestion>
"""


mturk = boto3.client('mturk', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY, region_name='us-east-1', endpoint_url=MTURK_SANDBOX)


def Create_Emotion_Distribution_collection_HIT(title):
    video = Experiment_Video.objects.filter(video_title = title)[0]
    video_prompt_num = video.video_prompt_num
    video_total_time = video.video_total_time
    task_time = int((video_total_time+video_prompt_num*TIME_FOR_EACH_PROMPT+TIME_FOR_TUTORIAL)/60)
    reward = format((video_total_time+video_prompt_num*TIME_FOR_EACH_PROMPT+TIME_FOR_TUTORIAL)/3600 * HOURLY_PAYMENT, '.2f')
    question = html_question.replace('_video_title_', title)
    question = question.replace('_condition_', "experiment1_distribution")
    new_hit = mturk.create_hit(
        Title = 'Emotion Labeling for a Video -'+title,
        Description = 'Watch a video, and label the emotion of a character in the video. About '+str(task_time)+' minutes task.',
        Keywords = 'video, emotion, labeling',
        Reward = str(reward),
        MaxAssignments = 50,
        QualificationRequirements = worker_requirements,
        LifetimeInSeconds = 7*24*60*60,
        AssignmentDurationInSeconds = 12*60*60,
        AutoApprovalDelayInSeconds = 3*24*60*60,
        Question = question,

    )
    return new_hit

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError
