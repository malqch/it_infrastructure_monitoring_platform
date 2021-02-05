<template>
    <div>
        <div class="wrapper">
            <el-row :span="24" class="serve_top">
                <el-col :span="8">
                    <div class="serve_top_r_t asset_center_height">
                        <p>物理服务器与虚拟服务器数量及占比</p>
                        <serverChart :id="server_info_table" :data="server_info_data"></serverChart>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="serve_top_r_t asset_center_height mr10">
                        <p>服务器操作系统数量及占比</p>
                        <operateSystemChart :id="operate_system_table" :data="operate_system_data"></operateSystemChart>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="serve_top_r_t asset_center_height">
                        <p>业务使用服务器数量及占比</p>
                        <businesschart :id="businessid" :data="business_device_count"></businesschart>
                    </div>
                </el-col>
            </el-row>
            <el-row :span="24"  class="serve_top">
                <el-col :span="24">
                    <div class="serve_top_r_t asset_center_height">
                        <serverVendorChart :id="server_vendor_table" :data="server_vendor_data"></serverVendorChart>
                    </div>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="10">
                    <div class="serve_top_r_t asset_center_height ml10">
                        <p>系统内各类资产数量</p>
                        <assetNumInfo :id="object_info_table" :data="object_info_data"></assetNumInfo>
                    </div>
                </el-col>
                <el-col :span="14">
                    <div class="serve_bottom_left mlr10">
                        <p>即将过保服务器</p>
                        <ServerExpireDevice :id="serverid" :data="server_info"></ServerExpireDevice>
                    </div>
                </el-col>
            </el-row>
            <el-row :span="24" class="mtb10">
                <el-col :span="24">
                    <div class="serve_bottom_left_info mr10">
                        <p>数据中心统计信息</p>
                        <RackRoomCount :id="datacenterid" :data="datacenter_info"></RackRoomCount>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<script>
    import assetNumInfo from "./assetVisualEchart/AssetNumInfo";
    import businesschart from './assetVisualEchart/BusinessChart';
    import RackRoomCount from './assetVisualEchart/RackRoomCount';
    import serverChart from './assetVisualEchart/ServerChart';
    import operateSystemChart from './assetVisualEchart/OperateSystemChart';
    import ServerExpireDevice from './assetVisualEchart/ServerExpireDevice';
    import serverVendorChart from './assetVisualEchart/ServerVendorChart';

    export default {
        name: 'ViewServe',
        components: {
            assetNumInfo,
            businesschart,
            RackRoomCount,
            serverChart,
            operateSystemChart,
            serverVendorChart,
            ServerExpireDevice,
        },
        data(){
            return{
                object_info_table:'object_info_table',
                object_info_data:null,
                business_device_count: [],
                businessid: "businessid",
                datacenter_info: [],
                datacenterid: 'datacenterid',
                server_info_table: 'server_info_table',
                server_info_data: [],
                operate_system_table: 'operate_system_table',
                operate_system_data: [],
                server_vendor_table: 'server_vendor_table',
                server_vendor_data: [],
                serverid: "serverid",
                server_info: [],
            }
        },
        computed: {
        },
        created() {
            this.optionData();
        },
        mounted() {
        },
        methods: {
                optionData(){
                this.$http.get(`asset/api/device/visualization/`, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res)=>{
                    const info_data=res.data.asset_info;
                    const info_xData=[];
                    const info_yData=[];
                    for(let item of info_data){
                        info_xData.push(item.device_type);
                        info_yData.push(item.device_type__count);
                    }
                    this.object_info_data={
                        xData:info_xData,
                        yData:info_yData
                    };
                    this.business_device_count = res.data.business_device_count;
                    this.datacenter_info = res.data.datacenter_info;
                    this.server_info_data = res.data.server_data;
                    this.operate_system_data = res.data.operate_system_data;
                    this.server_vendor_data = this.getData(res.data.vendor_dict);
                    this.server_info = res.data.expire_info
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 格式化数据
            getData(data) {
                let seriesDataObj = {} //每条数据
                let seriesData = []
                for(let item in data) {
                    seriesDataObj = {
                        name: item,
                        value: data[item],
                    }
                    seriesData.push(seriesDataObj)
                }
                return seriesData
            },
        },
        // beforeDestroy() {
        //     clearInterval(this.timer);
        // }
    }
</script>

<style lang="scss" scoped>
    @import "../../assets/css/fonts/font.css";
    @import "../../assets/scss/echarts";
    .wrapper{
        background: #191a2c;
    }
    .serve_top{
        border-radius: 10px;
        margin:10px;
    }
    .serve_bottom{
        margin:13px 0;
    }
    .serve_center,.serve_bottom{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .serve_center_left,.serve_center_right{
        height:200px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_center_left{
        margin:0 13px 0 20px;
    }
    dl{
        dt{
            color:#e5bb2e;
            display: inline;
        }
        .time{
            font-family:"DS-DIGI";
            font-size:26px;
        }
        .serve_name{
            font-size:16px;
        }
        dd{
            color:#fff;
            font-size:12px;
            margin-top:3px;
        }
    }
    .serve_top{
        margin:13px 13px;
    }
    .mr10{
        margin-left:10px;
    }
    .serve_top_r_t,.serve_top_r_b{
        height:200px;
        background:#24273e;
        border-radius: 10px;
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .serve_bottom_left,.serve_bottom_right{
        height:265px;
        background:#24273e;
        border-radius: 10px;
    }
    .serve_bottom_left_info{
        height:530px;
        background:#24273e;
        border-radius: 10px;
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .asset_center_height{
        height:265px;
    }
    .serve_bottom,.serve_bottom_left{
        p{
            color:#03c2ec;
            font-size:12px;
            padding:10px 0 0 10px;
            font-weight: 600;
        }
    }
    .top_font{
        text-align: center;
        padding-top: 10px;
    }
    .serve_top_char{
        height:70px;
        background:#24273e;
        border-radius: 10px;
    }
    .m10{
        margin:10px 0;
    }
</style>


