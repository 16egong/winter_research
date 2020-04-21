document.addEventListener("DOMContentLoaded", () => {
    if (time_in_min > 0) {
        console.log('time is greater than  0')
        start_timer(time_in_min);
    } else {
        var clock = document.getElementById('counter');
        var endtime = sessionStorage.getItem("endtime")
        var t = time_remaining(endtime);

        if(t.total<=0){ 
            clock.innerHTML = 'Time Left: '+0+': '+0;
        } else {
            run_clock(clock, endtime);
        }
    }
    
})


function start_timer(time_in_min) {
    var current_time = Date.parse(new Date());
    var endtime = new Date(current_time + time_in_min*60*1000);
    var clock = document.getElementById('counter');
    sessionStorage.setItem("endtime", endtime);
    run_clock(clock, endtime);
}


function time_remaining(endtime){
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor( (t/1000) % 60 );
    var minutes = Math.floor( (t/1000/60) % 60 );
    var hours = Math.floor( (t/(1000*60*60)) % 24 );
    var days = Math.floor( t/(1000*60*60*24) );
    return {'total':t, 'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds};
}

function run_clock(clock, endtime){
	function update_clock(){
		var t = time_remaining(endtime);
		clock.innerHTML = 'Time Left: '+t.minutes+': '+t.seconds;
		if(t.total<=0){ clearInterval(timeinterval); }
	}
	update_clock();
	var timeinterval = setInterval(update_clock,1000);
}
