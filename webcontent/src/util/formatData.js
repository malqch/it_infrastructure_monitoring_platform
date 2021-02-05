/**
 * Created by malq on 2020/6/17.
 */

// 按钮权限判断
export function hasBtnPermission(permission){
    let getBtnPermissionArr = JSON.parse(localStorage.getItem('btnPermission'));
    return getBtnPermissionArr.indexOf(permission) > -1;
}

// 树型数据转换
export function treeDataTranslate(data, id = 'id', pid = 'p_id') {
    var res = []
    var temp = {}
    for (var i = 0; i < data.length; i++) {
        temp[data[i][id]] = data[i]
    }
    for (var k = 0; k < data.length; k++) {
        if (temp[data[k][pid]] && data[k][id] !== data[k][pid]) {
            if (!temp[data[k][pid]]['children']) {
                temp[data[k][pid]]['children'] = []
            }
            if (!temp[data[k][pid]]['_level']) {
                temp[data[k][pid]]['_level'] = 1
            }
            data[k]['_level'] = temp[data[k][pid]]._level + 1
            temp[data[k][pid]]['children'].push(data[k])
        } else {
            res.push(data[k])
        }
    }
    return res
}

// 格式化数据
export function dataFormat(row) {
    if (row.roles === []) {
        return ''
    } else {
        var role = '';
        for (let v of row.roles)
        {
            role += '  ' + v.name;
        }
        return role
    }
}

// 获取当前时间并格式化（yyyy-MM-dd HH:mm:ss）
export function getFormatDate() {
    var date = new Date();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    return date.getFullYear() + "-" + month + "-" + strDate
        + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    // return currentDate;
}

export function formatDate(timestamp) {
    var date = new Date(timestamp);
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes() + ':';
    var s = date.getSeconds();
    return Y+M+D+h+m+s ;
}

//将时间戳转换成正常时间格式
export function timestampToTime(timestamp) {
    var date = new Date(timestamp * 1000);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    var Y = date.getFullYear() + '-';
    var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    var D = date.getDate() + ' ';
    var h = date.getHours() + ':';
    var m = date.getMinutes() + ':';
    var s = date.getSeconds();
    return Y+M+D+h+m+s;
}

export function datetimeFormat(row, column){
    const daterc = row[column.property]
    if(daterc!=null){
        const dateMat = new Date(daterc);
        const year = dateMat.getFullYear();
        const month = dateMat.getMonth() + 1;
        const day = dateMat.getDate();
        const hh = dateMat.getHours();
        const mm = dateMat.getMinutes();
        const ss = dateMat.getSeconds();
        const timeFormat = year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
        return timeFormat;
    }
}


