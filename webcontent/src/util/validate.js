/*是否合法IP地址*/
export function validateIP(rule, value,callback) {
    if(value==''||value==undefined||value==null){
        callback();
    }else {
        const reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
        if ((!reg.test(value)) && value != '') {
            callback(new Error('请输入正确的IP地址'));
        } else {
            callback();
        }
    }
}

/*是否合法Mac地址*/
export function validateMac(rule, value,callback) {
    if(value==''||value==undefined||value==null){
        callback();
    }else {
        const reg = /[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}/;
        if ((!reg.test(value)) && value != '') {
            callback(new Error('请输入正确的MAC地址'));
        } else {
            callback();
        }
    }
}

/*校验是否有中文*/
export function validateCh(rule, value, callback) {
    if(value==''||value==undefined||value==null){
        callback();
    }else {
        const reg = /[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
        if ((reg.test(value))) {
            callback(new Error('名称不能含有中文'));
        } else {
            callback();
        }
    }
}

/* 是否手机号码或者固话*/
export function validatePhoneTwo(rule, value, callback) {
    const reg = /^((0\d{2,3}-\d{7,8})|(1[34578]\d{9}))$/;
    if (value == '' || value == undefined || value == null) {
        callback();
    } else {
        if ((!reg.test(value)) && value != '') {
            callback(new Error('请输入正确的电话号码或者固话号码'));
        } else {
            callback();
        }
    }
}
// /* 是否固话*/
// export function validateTelphone(rule, value,callback) {
//     const reg =/0\d{2}-\d{7,8}/;
//     if(value==''||value==undefined||value==null){
//         callback();
//     }else {
//         if ((!reg.test(value)) && value != '') {
//             callback(new Error('请输入正确的固话（格式：区号+号码,如010-1234567）'));
//         } else {
//             callback();
//         }
//     }
// }
// /* 是否手机号码*/
// export function validatePhone(rule, value,callback) {
//     const reg =/^[1][3,4,5,7,8][0-9]{9}$/;
//     if(value==''||value==undefined||value==null){
//         callback();
//     }else {
//         if ((!reg.test(value)) && value != '') {
//             callback(new Error('请输入正确的电话号码'));
//         } else {
//             callback();
//         }
//     }
// }

/* 是否邮箱*/
export function validateEMail(rule, value,callback) {
    const reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
    if(value==''||value==undefined||value==null){
        callback();
    }else{
        if (!reg.test(value)){
            callback(new Error('请输入正确的邮箱地址'));
        } else {
            callback();
        }
    }
}
// /* 合法uri*/
// export function validateURL(textval) {
//     const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
//     return urlregex.test(textval);
// }
//
// 验证是否整数
export function isInteger(rule, value, callback) {
    if (!value) {
        return callback(new Error('输入不可以为空'));
    }
    setTimeout(() => {
        if (!Number(value)) {
            callback(new Error('请输入数字'));
        } else {
            const re = /^[0-9]*[1-9][0-9]*$/;
            const rsCheck = re.test(value);
            if (!rsCheck) {
                callback(new Error('请输入数字'));
            } else {
                callback();
            }
        }
    }, 0);
}
// 验证是否整数,非必填
// export function isIntegerNotMust(rule, value, callback) {
//     if (!value) {
//         callback();
//     }
//     setTimeout(() => {
//         if (!Number(value)) {
//             callback(new Error('请输入正整数'));
//         } else {
//             const re = /^[0-9]*[1-9][0-9]*$/;
//             const rsCheck = re.test(value);
//             if (!rsCheck) {
//                 callback(new Error('请输入正整数'));
//             } else {
//                 callback();
//             }
//         }
//     }, 1000);
// }
