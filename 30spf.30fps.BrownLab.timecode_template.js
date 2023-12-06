var secondsPerFrame = 30;
var currentFrame = timeToFrames();
var hours = 0; var minutes = 0; var seconds = 0;

function padNumber(x) {
    if(x<10){
        return "0" + x;
    } else {
        return x;
    }
}

seconds = currentFrame * secondsPerFrame % 60;
minutes = Math.floor(currentFrame * secondsPerFrame / 60 % 60);
hours = Math.floor(currentFrame * secondsPerFrame / 60 / 60);

padNumber(hours) + "h:" + padNumber(minutes) + "m";