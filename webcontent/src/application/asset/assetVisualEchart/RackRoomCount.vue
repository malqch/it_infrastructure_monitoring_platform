<template>
    <div class="box-container">
        <div :id=id :data=charts  class="echart-container"></div>
    </div>
</template>

<script>
    export default {
        name: "baseEchartsAllComponent",
        data(){
            return{
                charts: null,
                ChartLineGraph:null,
                datacenterdata: [],
                device_info: [],
                myChart:null
            }
        },
        watch:{
            data:{
                handler(newValue) {
                    this.datacenterdata = this.getData(newValue)
                    this.drawLineGraph(this.id,this.datacenterdata);
                },
                deep:true
            }

        },
        //接收父组件传过来的参数
        props:{
            id: {
                type: String,
                default: ''
            },
            data: {
                type: Array,
                default: null
            }
        },
        mounted() {
            if (this.data != null) {
                this.drawLineGraph(this.id, this.data);
            }
        },
        methods:{
            clickFun(param) {
                if(param.value === 0){
                    return;
                }
                if (typeof param.seriesIndex == 'undefined') {
                    return;
                }

                if (param.type == 'click') {
                    if (!param.data.hasChild) {
                        if (param.data.collapsed == undefined || param.data.collapsed == true) {
                            console.log("未定义或者是未展开，下次即将展开");
                            param.data.collapsed = false;
                        } else {
                            console.log("下次不展开");
                            param.data.collapsed = true;
                        }
                        return;
                    }
                    var arr = []
                    this.$http.get(`asset/api/device/rack_device_info/?rack_id=${param.data.rack_id}`, {
                                headers:{
                                    'token': localStorage.getItem('token')
                                }
                            }).then((res)=>{
                                var data_obj = res.data
                                for(let key in data_obj) {
                                    let obj = {}
                                    if(data_obj[key].device_type==="存储"){
                                        if(data_obj[key].controller_system_version === null){
                                            data_obj[key].controller_system_version = ''
                                        }
                                        if(data_obj[key].device_ip===null){
                                            data_obj[key].device_ip = ''
                                        }
                                        if(data_obj[key].device_vendor===null){
                                            data_obj[key].device_vendor = ''
                                        }
                                        if(data_obj[key].disk_capacity===null){
                                            data_obj[key].disk_capacity = ''
                                        }
                                        if(data_obj[key].controller_system_version===null){
                                            data_obj[key].controller_system_version = ''
                                        }
                                        if(data_obj[key].controller_num===null){
                                            data_obj[key].controller_num = ''
                                        }
                                        if(data_obj[key].controller_rack_disk_num===null){
                                            data_obj[key].controller_rack_disk_num = ''
                                        }
                                        if(data_obj[key].extension_rack_disk_num===null){
                                            data_obj[key].extension_rack_disk_num = ''
                                        }
                                        if(data_obj[key].host_port_num===null){
                                            data_obj[key].host_port_num = ''
                                        }
                                        if(data_obj[key].extension_port_num===null){
                                            data_obj[key].extension_port_num = ''
                                        }
                                        if(data_obj[key].extension_rack_num===null){
                                            data_obj[key].extension_rack_num = ''
                                        }
                                         obj = {
                                            name: data_obj[key].device_ip,
                                            value: null, //节点的值在tooltip显示
                                            children: [],
                                            tooltip: {
                                                trigger: "item",
                                                formatter: 'ip: ' + data_obj[key].device_ip + '<br/>' + '厂商: ' +
                                                    data_obj[key].device_vendor + '<br/>' + '磁盘大小: ' + data_obj[key].disk_capacity + '<br/>' +
                                                    '控制器系统版本: ' + data_obj[key].controller_system_version + '<br/>' + "控制器数量: " + data_obj[key].controller_num + '<br/>' +
                                                    "控制柜硬盘数量: " + data_obj[key].controller_rack_disk_num + '<br/>' + "扩展柜硬盘数量: " + data_obj[key].extension_rack_disk_num + '<br/>' +
                                                    "主机端口数量: " + data_obj[key].host_port_num + '<br/>' + "扩展端口数量: " + data_obj[key].extension_port_num + '<br/>' +
                                                    "扩展柜数量: " + data_obj[key].extension_rack_num + '<br/>' + "设备类型: "+ data_obj[key].device_type,
                                                textStyle: { //提示框的文本样式
                                                    fontSize: 10
                                                }
                                            }
                                        }
                                    }else{
                                        if(data_obj[key].device_ip===null){
                                            data_obj[key].device_ip = ''
                                        }
                                        if(data_obj[key].device_vendor===null){
                                            data_obj[key].device_vendor = ''
                                        }
                                        if(data_obj[key].operate_system===null){
                                            data_obj[key].operate_system = ''
                                        }
                                        if(data_obj[key].cpu_cores===null){
                                            data_obj[key].cpu_cores = ''
                                        }
                                        if(data_obj[key].memory_capacity===null){
                                            data_obj[key].memory_capacity = ''
                                        }
                                        if(data_obj[key].disk_capacity===null){
                                            data_obj[key].disk_capacity = ''
                                        }
                                        obj = {
                                            name: data_obj[key].device_ip,
                                            value: null, //节点的值在tooltip显示
                                            children: [],
                                            tooltip: {
                                                trigger: "item",
                                                formatter: 'ip: ' + data_obj[key].device_ip + '<br/>' + '厂商: ' +
                                                    data_obj[key].device_vendor + '<br/>' + '操作系统: ' +
                                                    data_obj[key].operate_system + '<br/>' + 'CPU核数: ' +
                                                    data_obj[key].cpu_cores + '<br/>' + '内存大小: ' + data_obj[key].memory_capacity +
                                                    '<br/>' + '磁盘大小: ' + data_obj[key].disk_capacity + '<br/>' + '设备类型: ' + data_obj[key].device_type,
                                                textStyle: { //提示框的文本样式
                                                    fontSize: 10
                                                }
                                            }
                                        }
                                    }
                                    arr.push(obj);
                                }
                        param.data.hasChild = false;
                        param.data.collapsed = false;
                        param.data.children = arr;
                        param.data.symbol = 'emptyCircle';
                        let data_info = this.myChart.getOption().series[0].data;
                        data_info=this.handle(data_info,0)
                        this.myChart.clear();
                        this.myChart.setOption({
                            type: "tree",
                            toolbox: { //工具栏
                                show: true,
                                iconStyle: {
                                    borderColor: "#03ceda"
                                },
                                feature: {
                                    restore: {}
                                }
                            },
                            grid: {
                                left: '5%',
                                right: '5%',
                                top: '10%',
                                bottom: '10%'
                            },
                            tooltip: {//提示框
                                trigger: "item",
                                triggerOn: "mousemove",
                                backgroundColor: "rgba(1,70,86,1)",
                                borderColor: "rgba(0,246,255,1)",
                                borderWidth: 0.5,
                                textStyle: {
                                    fontSize: 10
                                }
                            },
                            series: [
                                {
                                    type: 'tree',
                                    data: data_info,
                                    top: '0', //tree组件和边界上下左右的距离
                                    left: '5%',
                                    bottom: '0',
                                    right: '20%',
                                    layout: 'orthogonal', //选择的展示图类型
                                    // layout: "radial",
                                    symbolSize: 10,
                                    roam: 'move',  // //是否开启鼠标缩放和平移漫游。scale/move/true
                                    initialTreeDepth: 3, // 打开的层数
                                    itemStyle: {
                                        borderWidth: 2, //节点圆圈边缘的宽度
                                    }, // 树图中每个节点的颜色
                                    label: { //节点对应的文本样式
                                        // fontSize: 12, // 设置字体大小
                                        fontFamily: "SourceHanSansCN", // 文字的字体
                                        position: "right", // 文本位置
                                        color: '#03c2ec'
                                    },
                                    animationDurationUpdate: 750,  //展开速度
                                    expandAndCollapse: true,
                                    animationDuration: 100,
                                }
                            ]

                        })
                    })
                }},
            handle(data,index,color='#00f6ff') {
                var colors=[
                    '#ffdb5c',
                    '#ff9f7f',
                    '#fb7293',
                    '#37a2da',
                    '#9fe6b8',
                    "#B62AFF",
                    "#95F300",
                    "#04FDB8",
                    "#AF5AFF",
                    "#8529d5",
                ]
                //index标识第几层
                return data.map((item,index2)=>{
                    //计算出颜色
                    if(index==1){
                        color = colors.find((item, eq) => eq == index2 % 10);
                    }
                    // 设置线条颜色
                    item.lineStyle= { color: color }
                    // 设置节点颜色
                    // consolesole.log(item, item.children, 44444)
                    if (item.children.length!=0) {//存在子节点
                        item.itemStyle = {
                            borderColor: color,
                            color:color
                        };
                        item.children=this.handle(item.children,index+1,color)
                    } else {//不存在
                        if(item.value!=0){
                            item.itemStyle = {
                                color:color,
                                borderColor: color
                            };
                            item.symbol ='circle';  //设置节点圆圈颜色
                        }else{
                            item.itemStyle = {
                                color:'transparent',
                                borderColor: color
                            };
                        }

                    }
                    return item
                })
            },
            getData(charts) {
                let data = {
                    name: "数据中心",
                    value: charts.length,
                    children: [],
                    tooltip: {
                        trigger: "item",
                        formatter: '数据中心数量:' +charts.length,
                        textStyle: { //提示框的文本样式
                            fontSize: 10
                        }
                    }
                };
                // 遍历数据中心
                charts.forEach(item =>{
                    let obj = {
                        name: item.datacenter_name,
                        value: item.num_room,
                        children: [],
                        tooltip: {
                            trigger: "item",
                            formatter: "数据中心：" + item.datacenter_name+'<br/>'+'机房数量: '+item.num_room,
                            textStyle: { //提示框的文本样式
                                fontSize: 10
                            }
                        },
                        datacenterid: item.datacenter_id
                    };
                    item.room_info.forEach(room_item =>{
                        let obj2 = {
                            name: room_item.room_name,
                            value: room_item.num_rack,
                            children: [],
                            tooltip: {
                                trigger: "item",
                                formatter: "数据中心: " + item.datacenter_name+'<br/>'+"机房: " + room_item.room_name+ '<br/>' + '机柜数量: '+room_item.num_rack,
                                textStyle: { //提示框的文本样式
                                    fontSize: 10
                                }
                            },
                            room_id: room_item.room_id
                        };
                        room_item.rack_info.forEach(rack_item =>{
                            let obj3 = {
                                name: rack_item.location_cabinet,
                                value: rack_item.num_device,
                                children: [],
                                hasChild: true,
                                collapsed: true,
                                tooltip: {
                                    trigger: "item",
                                    // formatter: "数据中心: " + item.datacenter_name+'<br/>'+"机房: " + room_item.room_name+'<br/>'+ "机柜: " + rack_item.location_cabinet+'<br/>'+'设备数量: '+rack_item.num_device,
                                    formatter: "数据中心: " + item.datacenter_name+'<br/>'+"机房: " + room_item.room_name+'<br/>'+ "机柜: " +
                                        rack_item.location_cabinet+'<br/>'+'服务器数量: '+rack_item.device_num +'<br/>'+'存储数量: '+rack_item.storage_num +
                                    '<br/>'+'网络设备数量: '+rack_item.network_num,

                                    textStyle: { //提示框的文本样式
                                        fontSize: 10
                                    }
                                },
                                rack_id: rack_item.rack_id
                            };
                            obj2.children.push(obj3)
                        })
                        obj.children.push(obj2);
                        })
                    data.children.push(obj);
                })
                let arr=[]
                arr.push(data)
                arr=this.handle(arr,0)
                return arr;
                // this.datacenterdata = arr
            },
            drawLineGraph(id,charts){
                this.myChart = this.$echarts.init(document.getElementById(id));
                this.myChart.on("click", this.clickFun);
                this.optionBusiness= {
                    type: "tree",
                    toolbox: { //工具栏
                        show: true,
                        iconStyle: {
                            borderColor: "#03ceda"
                        },
                        feature: {
                            restore: {}
                        }
                    },
                    grid:{
                        left:'5%',
                        right:'5%',
                        top:'10%',
                        bottom:'10%'
                    },
                    tooltip: {//提示框
                        trigger: "item",
                        triggerOn: "mousemove",
                        backgroundColor: "rgba(1,70,86,1)",
                        borderColor: "rgba(0,246,255,1)",
                        borderWidth: 0.5,
                        textStyle: {
                            fontSize: 10
                        }
                    },
                    series: [
                        {   type: 'tree',
                            data: charts,
                            top: '0', //tree组件和边界上下左右的距离
                            left: '5%',
                            bottom: '0',
                            right: '20%',
                            layout : 'orthogonal', //选择的展示图类型
                            // layout: "radial",
                            symbolSize:10,
                            roam: 'move',  // //是否开启鼠标缩放和平移漫游。scale/move/true
                            initialTreeDepth: 3, // 打开的层数
                            itemStyle: {
                                borderWidth: 2, //节点圆圈边缘的宽度
                            }, // 树图中每个节点的颜色
                            label: { //节点对应的文本样式
                                // fontSize: 12, // 设置字体大小
                                fontFamily: "SourceHanSansCN", // 文字的字体
                                position: "right", // 文本位置
                                color:'#03c2ec'
                            },
                            animationDurationUpdate: 750,  //展开速度
                        }
                    ]

                };
                this.myChart.setOption(this.optionBusiness);
                setTimeout(function() {
                    window.addEventListener('resize', ()=> {
                        this.myChart.resize();
                    })
                }, 200)
            }
        },
        beforeDestroy() {
            clearInterval(this.ChartLineGraph);
            this.ChartLineGraph = null;
        }
    }

</script>

<style lang="scss" scoped>
    .echart-container {
        height: 470px;
    }
</style>
