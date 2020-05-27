var TimeZone = [
    // ["UTC","UTC"],
    // ["UTC+1","UTC+1"],
    // ["UTC+2","UTC+2"],
    // ["UTC+3","UTC+3"],
    // ["UTC+4","UTC+4"],
    // ["UTC+5","UTC+5"],
    // ["UTC+6","UTC+6"],
    // ["UTC+7","UTC+7"],
    ["Asia/Shanghai","中国(泸深,香港)"],
    // ["UTC+9","UTC+9"],
    // ["UTC+10","UTC+10"],
    // ["UTC+11","UTC+11"],
    // ["UTC-11","UTC-11"],
    // ["UTC-10","UTC-10"],
    // ["UTC-9","UTC-9"],
    // ["UTC-8","UTC-8"],
    // ["UTC-7","UTC-7"],
    // ["UTC-6","UTC-6"],
    // ["UTC-5","UTC-5"],
    ["America/New_York","美国纽约"],
    // ["UTC-3","UTC-3"],
    // ["UTC-2","UTC-2"],
    // ["UTC-1","UTC-1"],
];

var Interval = [
    [
        [{name:"weeks",placeholder:"间隔周"},"周"],
        [{name:"days",placeholder:"间隔日"},"日"],
        [{name:"hours",placeholder:"间隔小时"},"小时"],
    ],
    [
        [{name:"minutes",placeholder:"间隔分钟"},"分钟"],
        [{name:"seconds",placeholder:"间隔秒"},"秒"],
    ]
];

var Cron = [
    [
        [{name:"year",placeholder:"1990"},"年"],
        [{name:"month",placeholder:"1-12"},"月"],
        [{name:"day",placeholder:"1-31"},"日"],
    ],
    [
        [{name:"hour",placeholder:"0-23"},"时"],
        [{name:"minute",placeholder:"0-59"},"分"],
        [{name:"second",placeholder:"0-59"},"秒"],
    ],
    [
        [{name:"week",placeholder:"0-53"},"周"],
        ["星期",{name:"day_of_week",placeholder:"0-6"}],
    ],
];

export {
    TimeZone,Interval,Cron
}