<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
<!--            <el-row type="flex" class="row-bg" justify="space-between">-->
<!--                <div>-->
<!--                    <el-button-->
<!--                            type="primary"-->
<!--                            icon="el-icon-circle-plus-outline"-->
<!--                            @click="handleCreate">导入模板</el-button>-->
<!--                </div>-->
<!--            </el-row>-->
            <div style="padding-bottom: 15px;">
                <span>华为云环境：</span>
                <el-select v-model="huaweiyun_env" @change="handleSelectHuaweiEnv" style="width: 130px;" placeholder="请选择华为云环境">
                    <el-option
                            v-for="item in huaweiyun_options"
                            :key="item.id"
                            :label="item.hw_ip"
                            :value="item.hw_ip">
                    </el-option>
                </el-select>
            </div>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="name" label="名称" align="center"></el-table-column>
                <el-table-column prop="id" label="ID" align="center"></el-table-column>
                <el-table-column prop="arch" label="CPU架构" align="center"></el-table-column>
                <el-table-column prop="os_type" label="OS类型" :formatter="osTypeFormat" align="center"></el-table-column>
                <el-table-column prop="cpu" label="CPU核数" align="center"></el-table-column>
                <el-table-column prop="memory" label="内存大小(MB)" align="center"></el-table-column>
                <el-table-column prop="disks" label="磁盘总大小(GB)" align="center"></el-table-column>
            </el-table>
<!--            <div class="pagination">-->
<!--                <el-pagination-->
<!--                        background-->
<!--                        layout="total, prev, pager, next"-->
<!--                        :current-page="query.pageIndex"-->
<!--                        :page-size="query.pageSize"-->
<!--                        :total="pageTotal"-->
<!--                        @current-change="handlePageChange"-->
<!--                ></el-pagination>-->
<!--            </div>-->
        </div>
    </div>
</template>

<script>
    import { datetimeFormat } from '../../../util/formatData'
    export default {
        data() {
            return {
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                huaweiyun_env_info: '',
                huaweiyun_env: '',
                title: '',
                windows_os_version: [],
                linux_os_version: [],
                other_os_version: [],
                huaweiyun_options: [],
                editVisible: false,
                deleteVisible: false,
                datetimeFormat: null,
                loading: true,
                pageTotal: 0,
                form: {},
                idx: -1,
                id: -1,
            };

        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getHuaweiyunData();
            this.datetimeFormat = datetimeFormat;
        },
        methods: {
            // 格式化虚拟机类型
            osTypeFormat(row) {
                if(row.os_type.osType==='Windows') {
                    for(let i = 0; i < this.windows_os_version.length; i++){
                        if(this.linux_os_version[i].os_id===row.os_type.osVersion){
                            return this.linux_os_version[i].os_version;
                        }
                    }
                }else if(row.os_type.osType==='Linux') {
                    for(let i = 0; i < this.linux_os_version.length; i++){
                        if(this.linux_os_version[i].os_id===row.os_type.osVersion){
                            return this.linux_os_version[i].os_version;
                        }
                    }
                }else if(row.os_type.osType==='Other') {
                    for(let i = 0; i < this.other_os_version.length; i++){
                        if(this.linux_os_version[i].os_id===row.os_type.osVersion){
                            return this.linux_os_version[i].os_version;
                        }
                    }
                }
            },
            // 获取华为云环境数据
            getHuaweiyunData() {
                this.$http.get(`automation/api/huawei/`, {
                    headers: {
                        'token': this.token,
                    }
                }).then((res) => {
                    if(sessionStorage.getItem('huaweiyun_env')) {
                        this.huaweiyun_env = JSON.parse(sessionStorage.getItem('huaweiyun_env')).hw_ip;
                    }else {
                        sessionStorage.setItem('huaweiyun_env', JSON.stringify(res.data[0]));
                        this.huaweiyun_env = res.data[0].hw_ip;
                    }
                    this.huaweiyun_options = res.data;
                    this.getData();
                    this.getOsType();
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 获取虚拟机模板数据
            getData() {
                this.$http.get('automation/api/huawei/vms/?Template=true', {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    res.data.vms.map( item =>{
                        item['id']=item['uri'].split("/")[5];
                        item['cpu']=item['vmConfig'].cpu.quantity;
                        item['memory']=item['vmConfig'].memory.quantityMB;
                        item['disks']=item['vmConfig'].disks[0].quantityGB;
                        item['os_type']=item['osOptions'];
                    });
                    this.tableData = res.data.vms;
                    this.pageTotal = res.data.total;
                    this.loading = false;
                }).catch(  (error) =>{
                    console.log(error);
                    this.$message.error('查询失败！');
                    this.loading = false;
                });
            },
            // 触发选择环境操作
            handleSelectHuaweiEnv(val) {
                this.tableData = [];
                this.handleSetHuaweiEnvInfo(val);
                sessionStorage.setItem('huaweiyun_env', JSON.stringify(this.huaweiyun_env_info));
                this.getData();
            },
            handleSetHuaweiEnvInfo(val) {
                for(var j = 0, len=this.huaweiyun_options.length; j < len; j++) {
                    if(this.huaweiyun_options[j].hw_ip===val) {
                        return this.huaweiyun_env_info = this.huaweiyun_options[j];
                    }
                }
            },
            // 查询操作系统版本
            getOsType() {
                this.$http.get(`automation/api/huawei/vms/osversions/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.windows_os_version = res.data.windows;
                    this.linux_os_version = res.data.linux;
                    this.other_os_version = res.data.other;
                }).catch(  (error) => {
                    console.log(error);
                    this.$message.error(this.$message.error('查询失败！'));
                });
            },
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            // 新增操作
            handleCreate() {
                this.form = {};
                this.title = "新增";
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$http.post(`automation/api/script/`,
                            this.form,
                            {
                                headers:{
                                    'token': this.token,
                                    'env': sessionStorage.getItem('huaweiyun_env')
                                }
                            }).then((res)=>{
                            if(res.status === 200 || res.status === 201) {
                                this.$message.success('创建成功！');
                                this.editVisible = false;
                                this.getData();
                            }else{
                                this.$message.success('创建失败！');
                            }
                        }).catch( (error) =>{
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                    } else {
                        this.$message.warning('请选择必填项');
                        return false;
                    }
                });
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
        },
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    @import "../../../../public/tinymce/skins/ui/oxide/skin.css";
    .tag_margin{
        margin:5px 5px 0 0;
    }
    .handle-box {
        margin-bottom: 20px;
    }
    .handle-select {
        width: 120px;
    }
    .handle-input {
        width: 300px;
        display: inline-block;
    }
    .table {
        width: 100%;
        font-size: 14px;
    }
    .red {
        color: #ff0000;
    }
    .mr10 {
        margin-right: 10px;
    }
    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>
