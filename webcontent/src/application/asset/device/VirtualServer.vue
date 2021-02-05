<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 虚拟服务器
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="searchData">
                <el-row class="margin_bot">
                    <el-row type="flex" class="row-bg" justify="space-around">
                        <el-col>
                            <el-button
                                    type="primary"
                                    icon="el-icon-edit"
                                    @click="handleAdd()"
                                    class="handle-box"
                                    plain
                            >增加
                            </el-button>
                            <el-button @click="exportData" type="danger" plain>导出Excel
                            </el-button>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="2">
                            <el-button class="mr10" @click="exportTemplate" type="info" plain>下载模版
                            </el-button>
                        </el-col>
                        <el-col :span="18">
                            <el-upload
                                    class="upload-demo inlineB"
                                    ref="uploadExcel"
                                    :action="uploadUrl"
                                    :headers="headers"
                                    :limit="1"
                                    :auto-upload="false"
                                    :on-success="uploadSuccess"
                                    :on-error="handleError">
                                <el-button slot="trigger" size="small" type="warning" plain>选取文件</el-button>
                                <el-button style="margin-left: 10px;" size="small" type="success" plain @click="importExcel">上传到服务器</el-button>
                                <div slot="tip" class="el-upload__tip"></div>
                            </el-upload>
                        </el-col>
                    </el-row>
                </el-row>
                <el-row>
                    <el-col :span="4">
                        <el-form-item>
                            <el-input v-model="searchData.virtual_ip" clearable placeholder="ip"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item>
                            <el-input v-model="searchData.hostname" clearable placeholder="名称"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item>
                            <el-input v-model="searchData.status" clearable placeholder="状态"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item>
                            <el-select style="width:100%" v-model="searchData.type" placeholder="请选择类型" clearable>
                                <el-option
                                        v-for="item in typeOptions"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-form-item>
                            <el-select v-model="searchData.asset_manager" placeholder="资产管理者" @focus="queryStaff" clearable>
                                <el-option
                                        v-for="item in assetStaffData"
                                        :key="item.id"
                                        :label="item.username"
                                        :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="4">
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </el-col>
                </el-row>
            </el-form>
           <el-table
                   v-loading="loading"
                :data="tableData"
                border
                ref="table"
                style="width: 100%"
           >
<!--            <el-table-column fixed width="50" type="selection" align="center"></el-table-column>-->

               <el-table-column width="50" type="index" label="序号" align="center"></el-table-column>
               <af-table-column prop="hostname" label="名称" align="center"></af-table-column>
               <af-table-column prop="virtual_ip" label="IP" align="center"></af-table-column>
               <af-table-column prop="type" label="虚拟化类型 " align="center"></af-table-column>
               <af-table-column prop="status" label="状态" align="center"></af-table-column>
               <af-table-column prop="operate_system" label="操作系统" align="center"></af-table-column>
               <af-table-column prop="operate_system_version" label="操作系统版本" align="center"></af-table-column>
               <af-table-column prop="cpu_cores" label="cpu核数" align="center"></af-table-column>
               <af-table-column prop="memory_capacity" label="内存容量(G)" align="center"></af-table-column>
               <af-table-column prop="disk_capacity" label="磁盘容量(G)" align="center"></af-table-column>
               <af-table-column prop="is_monitor" label="是否监控" align="center"></af-table-column>
               <af-table-column prop="server_belong_business" label="所属业务" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchBusiness(scope.row)" class="color-link">查看业务</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="label" label="标签" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchLabel(scope.row)" class="color-link">查看标签</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="network" label="网卡信息" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchNetwork(scope.row)" class="color-link">查看网卡信息</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="username" label="管理用户名" align="center"></af-table-column>
               <af-table-column prop="snmp_username" label="snmp用户名" align="center"></af-table-column>
               <af-table-column prop="usage" label="用途" align="center"></af-table-column>
               <af-table-column prop="update_time" label="更新时间" align="center" :formatter="dateFormat"></af-table-column>
               <af-table-column prop="asset_manager.username" label="资产管理者" align="center"></af-table-column>
               <el-table-column fixed="right" label="操作" width="200" align="center">
                <template slot-scope="scope">
                    <el-button
                        type="text"
                        icon="el-icon-edit"
                        @click="handleEdit(scope.row)"
                    >编辑
                    </el-button>
                    <el-button
                        type="text"
                        icon="el-icon-delete"
                        class="red"
                        @click="handledelete(scope.row)"
                    >删除
                    </el-button>
                    <el-button
                            type="text"
                            icon="el-icon-s-goods"
                            @click="handlemaintain(scope.row)"
                    >维护 {{ scope.row.maintain_status }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <div class="pagination">
            <el-pagination
                    background
                    layout="total, prev, pager, next"
                    :current-page="query.pageIndex"
                    :page-size="query.pageSize"
                    :total="pageTotal"
                    @current-change="handlePageChange"
            ></el-pagination>
        </div>

        </div>
        <el-dialog :title="makeTitle" :visible.sync="editVisible" width="50%">
            <el-form ref="form" :rules="rules" :model="form" class="demo-ruleForm" label-width="100px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="名称" prop="hostname">
                            <el-input v-model="form.hostname"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="ip" prop="virtual_ip">
                            <el-input v-model="form.virtual_ip"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="内存容量" prop="memory_capacity">
                            <el-input type="number" v-model.number="form.memory_capacity"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="磁盘容量" prop="disk_capacity">
                            <el-input type="number" v-model="form.disk_capacity"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="cpu核数">
                            <el-input v-model="form.cpu_cores"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="操作系统">
                            <el-select style="width:100%" v-model="form.operate_system" placeholder="请选择操作系统" clearable>
                                <el-option
                                        v-for="item in operatesystemOptions"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="操作系统版本">
                            <el-input v-model="form.operate_system_version"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="虚拟化类型">
                            <el-select style="width:100%" v-model="form.type" placeholder="请选择虚拟化类型" clearable>
                                <el-option
                                        v-for="item in typeOptions"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="状态">
                            <el-select style="width:100%" v-model="form.status" placeholder="请选择状态" clearable>
                                <el-option
                                        v-for="item in statusOptions"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="用途">
                            <el-input v-model="form.usage"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="ssh用户名">
                            <el-input v-model="form.username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="ssh密码">
                            <el-input v-model="form.password"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="ssh端口" prop="ssh_port">
                            <el-input v-model="form.ssh_port"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="snmp用户名">
                            <el-input v-model="form.snmp_username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="snmp密码">
                            <el-input v-model="form.snmp_password"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="所属业务">
                            <el-select style="width:100%" value-key="id"  v-model="form.belong_business" placeholder="请选择所属业务" @focus="querybusiness()" multiple>
                                <el-option v-for="item in businessData"
                                           :key=item.id
                                           :label="item.name"
                                           :value=item.name>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="标签">
                            <el-select style="width:100%" value-key="id"  v-model="form.label" placeholder="请选择标签" @focus="querylabel" multiple>
                                <el-option v-for="item in labelData"
                                           :key=item.id
                                           :label="item.tag_name"
                                           :value=item.tag_name>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="是否监控">
                            <el-select style="width:100%" v-model="form.is_monitor" placeholder="请选择" clearable>
                                <el-option
                                        v-for="item in is_monitor_options"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="资产管理者">
                            <el-select style="width:100%" v-model="form.asset_manager" placeholder="请选择" @focus="queryStaff" clearable>
                                <el-option
                                        v-for="item in assetStaffData"
                                        :key="item.id"
                                        :label="item.username"
                                        :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form ref="querynetworkData" :rules="networkrules" :model="querynetworkData[0]" label-width="85px" :hide-required-asterisk="true">
                            <el-form-item label="网卡信息">
                                <el-row :gutter="24">
                                    <el-col :span="18" class="net_bg">
                                        <el-row v-for="(item, index) in querynetworkData" :key="item.id">
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="mac" prop="mac">
                                                    <el-input v-model="querynetworkData[index].mac"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-form-item label="netmask">
                                                    <el-input v-model="querynetworkData[index].netmask"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="ip" prop="ip">
                                                    <el-input v-model="querynetworkData[index].ip"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-form-item label="broadcast">
                                                    <el-input v-model="querynetworkData[index].broadcast"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="type">
                                                    <el-select v-model="querynetworkData[index].type" clearable>
                                                        <el-option
                                                                v-for="item in networkType"
                                                                :key="item.value"
                                                                :label="item.value"
                                                                :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-button
                                                        @click="del(index)"
                                                        size="small"
                                                        class="margin_26"
                                                        type="danger" plain
                                                ><i class="el-icon-delete"></i></el-button>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-button
                                                @click="addItem"
                                                size="small"
                                                icon="el-icon-circle-plus"
                                                class="margin_26"
                                                type="primary" plain
                                        ></el-button>
                                    </el-col>
                                </el-row>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="所属业务" :visible.sync="businessVisible" width="30%" class="alert_dialog">
            <ul :model="businessSingleDATA[0]" v-for="item in businessSingleDATA" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">业务名称:</label>
                    <span class="network_span">{{item.name}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">业务负责人:</label>
                    <span class="network_span">{{item.staff.username}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">邮箱:</label>
                    <span class="network_span">{{item.staff.email}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">电话:</label>
                    <span class="network_span">{{item.staff.phone}}</span>
                </li>
            </ul>
        </el-dialog>
        <el-dialog title="网卡信息" :visible.sync="networkVisible" width="35%" class="alert_dialog">
            <ul :model="querynetworkData[0]" v-for="item in querynetworkData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">mac:</label>
                    <span class="network_span">{{item.mac}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">netmask:</label>
                    <span class="network_span">{{item.netmask}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">ip:</label>
                    <span class="network_span">{{item.ip}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">broadcast:</label>
                    <span class="network_span">{{item.broadcast}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">type:</label>
                    <span class="network_span">{{item.type}}</span>
                </li>
            </ul>
        </el-dialog>
        <el-dialog title="标签" :visible.sync="labelVisible" width="30%" class="alert_dialog">
            <ul :model="labelSingleData[0]" v-for="item in labelSingleData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">标签名称:</label>
                    <span class="network_span">{{item.tag_name}}</span>
                </li>
            </ul>
        </el-dialog>

    </div>
</template>

<script>
    import { validateIP, validateMac, validateCh, isInteger } from "../../../util/validate";

    export default {
        name: "server",
        data() {
            return{
                tableData: [],
                editVisible: false,
                businessVisible: false,
                networkVisible: false,
                labelVisible: false,
                form: {},
                id: -1,
                businessData: [],
                businessSingleDATA: [{
                    name: "",
                    email: "",
                    staff:{"username":"", "email": "", "phone":""}
                }],
                networkData: { items: [{}] },
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                searchData: {
                    hostname: "",
                    status: '',
                    type:"",
                    virtual_ip: "",
                    asset_manager: ""
                },
                querynetworkData: [{}],
                makeTitle: '',
                exportDataRes: [],
                typeOptions:[{
                    value: 'H3C'
                },{
                    value: 'HUAWEI'
                }, {
                    value: 'VMWARE'
                }],
                statusOptions:[{
                    value: "使用"
                },{
                    value: "未使用"
                }],
                vendorData:[{
                    value: "华为"
                },{
                    value: "联想"
                }],
                roomData:[],
                rackData:[],
                datacenterData: [],
                labelData: [],
                labelSingleData:[],
                assetStaffData: [],
                dcName: "",
                roomName: "",
                data_center_id: "",
                location_zone_id: "",
                asset_manager_id: "",
                headers:{
                    'token': localStorage.getItem('token')
                },
                uploadUrl: 'asset/api/virtual_server/excel/',
                networkType: [{
                    value: "内网"
                },{
                    value: "公网"
                }],
                rules: {
                    virtual_ip: [
                        {required: true, message: 'ip不能为空', trigger: 'blur'},
                        { validator: validateIP, trigger: 'blur'},
                    ],
                    memory_capacity: [
                        { required: true, message: '请输入内存容量', trigger: 'blur'},
                    ],
                    disk_capacity: [
                        { required: true, message: '请输入磁盘容量', trigger: 'blur'},
                    ],
                    hostname: [
                        { required: true, message: '请输入主机名', trigger: 'blur'},
                        // { validator: validateCh, trigger: 'blur'},
                    ],
                    ssh_port: [
                        { required: false, message: '请输入端口', trigger: 'blur'},
                        { validator: isInteger, trigger: 'blur'},
                    ],
                },
                networkrules:{
                    ip: [
                        {required: true, message: 'ip不能为空'},
                        { validator: validateIP, trigger: 'blur'},
                    ],
                    mac: [
                        {required: true, message: 'mac地址不能为空'},
                        {validator: validateMac, trigger: 'blur'}
                    ]
                },
                operatesystemOptions: [{
                    value: 'Windows'
                },{
                    value: 'Neokylin'
                },{
                    value: 'SUSE'
                }, {
                    value: 'RedHat'
                }, {
                    value: 'Centos'
                }, {
                    value: 'Ubuntu'
                }
                ],
                is_monitor_options:[{
                    value: "是"
                },{
                    value: "否"
                }],
                loading: true
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.$http.get(`asset/api/virtual_server/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&hostname=${this.searchData.hostname}&status=${this.searchData.status}&type=${
                    this.searchData.type}&virtual_ip=${this.searchData.virtual_ip}&asset_manager=${this.searchData.asset_manager}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        this.tableData = res.data['data'];
                        this.pageTotal = res.data['total_count'];
                        this.loading = false
                }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                        this.loading = false
                    });
            },
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.makeTitle = "编辑";
                this.form = JSON.parse( JSON.stringify(row));
                this.$http.get(`asset/api/network/virtual_networks/?virtual_server_id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        this.querynetworkData = res.data
                    });
                this.labelData = row.label
                this.businessData = row.belong_business
                var form_label_name = []
                for (var labelindex in this.labelData) {
                    form_label_name.push(this.labelData[labelindex].tag_name)
                }
                // 将新的Number数组，绑定到select空间的v-model上
                this.form.label = form_label_name
                if(row.ssh_port===undefined){
                    this.form.ssh_port = 22
                }
                var form_business_name = []
                for (var businessindex in this.businessData) {
                    form_business_name.push(this.businessData[businessindex].name)
                }
                if(row.asset_manager) {
                    this.asset_manager_id  = row.asset_manager.id;
                    this.form.asset_manager = row.asset_manager.username;
                }
                // 将新的Number数组，绑定到select空间的v-model上
                this.form.belong_business = form_business_name;
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$set(this.form, 'network', this.querynetworkData)
                    if(this.form.memory_capacity==undefined){
                        this.$message.error("内存容量为必传参数")
                        return
                    }
                    if(this.form.disk_capacity==undefined) {
                        this.$message.error("磁盘容量为必传参数")
                        return
                    }
                    if(this.makeTitle=="增加"){
                        this.$http.post(`asset/api/virtual_server/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            if (res.status === 201) {
                                this.editVisible = false
                                console.log('Response:' + JSON.stringify(res));
                                this.$message.success('保存成功！');
                                this.form = {};
                                this.getData()
                            } else {
                                this.$message.error('保存失败！');
                            }
                        }).catch( (error) =>{
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }else{
                        if(this.form.asset_manager && typeof this.form.asset_manager != "number"){
                            this.$set(this.form, 'asset_manager', this.asset_manager_id)
                        }
                        this.$http.put(`asset/api/virtual_server/${this.id}/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success('修改成功');
                            this.getData()
                        }).catch( (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                })//校验通过执行
            },
            //新增弹框
            handleAdd() {
                this.form = {
                    ssh_port: 22
                };
                this.makeTitle = "增加";
                this.editVisible = true;
                this.querynetworkData = [{}];
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            //查询业务信息
            querybusiness() {
                this.$http.get(`asset/api/business/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.businessData = res.data
                })
            },
            //增加网卡数量
            addItem() {
                this.networkData.items.push({
                    mac: '',
                    broadcast: '',
                    netmask: '',
                    ip: '',
                    type: ''
                })
                this.querynetworkData.push({
                    mac: '',
                    broadcast: '',
                    netmask: '',
                    ip: '',
                    type: ''
                })
            },
            //网卡数量减少
            del(index) {
                this.networkData.items.splice(index, 1);
                this.querynetworkData.splice(index, 1)
            },
            //分页
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            searchBusiness(row) {
                if(row.belong_business!=""){
                    this.businessSingleDATA = row.belong_business
                    for (var p in this.businessSingleDATA) {//遍历json数组时，这么写p为索引，0,1
                        if(this.businessSingleDATA[p].staff==null){
                            this.businessSingleDATA[p].staff = {"username":"", "email": "", "phone":""}
                        }
                    }
                    this.businessVisible = true
                }else{
                    this.$message.warning('业务信息不存在');
                }
            },
            //查看标签
            searchLabel(row) {
                if(row.label!=""){
                    this.labelSingleData = row.label
                    this.labelVisible = true
                    }else{
                        this.$message.warning('标签信息不存在');
                    }
                 },
            searchNetwork(row) {
                this.$http.get(`asset/api/network/virtual_networks/?virtual_server_id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.querynetworkData = res.data
                    if(this.querynetworkData==""){
                        this.$message.warning('网卡数据不存在');
                    }else{
                        this.networkVisible = true
                    }
                });
            },
            handledelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.delete(`asset/api/virtual_server/${row.id}/`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex', 1)
                        this.getData()
                    } else {
                        this.$message.error(res.data.msg);
                    }

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            })},
            // 导出模版
            exportTemplate() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["名称", "类型","状态", "用途","服务器用户名","服务器密码","snmp用户名","snmp密码", "操作系统","系统版本",
                        "cpu核数","内存容量","磁盘容量","ip"];// 上面设置Excel的表格第一行的标题

                    const list = []
                    export_json_to_excel(tHeader, list, "虚拟机导入模版");   //标题，数据，文件名
                });
            },
            // 导出数据
            exportData() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["ip","名称", "类型","状态", "用途","服务器用户名","服务器密码","snmp用户名","snmp密码", "操作系统","系统版本",
                        "cpu核数","内存容量","磁盘容量", "创建时间", "资产管理者"];// 上面设置Excel的表格第一行的标题

                    const filterVal = ["virtual_ip","hostname", "type","status", "usage", "username", "password", "snmp_username", "snmp_password",
                        "operate_system", "operate_system_version",  "cpu_cores", "memory_capacity", "disk_capacity",
                    "create_time", "asset_manager"]; // 上面的是tableData里对象的属性

                    this.$http.get(`asset/api/virtual_server/?hostname=${this.searchData.hostname}&status=${this.searchData.status}&type=${this.searchData.type}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.exportDataRes = res.data;
                    }).then(() =>{
                        const list = this.exportDataRes;              //把data里的tableData存到list
                        const data = this.formatJson(filterVal, list);

                        export_json_to_excel(tHeader, data, "虚拟机服务器");   //标题，数据，文件名
                    })});
            },
            formatJson(filterVal, jsonData) {
                const data_list = []
                jsonData.map((v) => {
                    if(v.asset_manager!=null){
                        v.asset_manager = v.asset_manager.username
                    }
                    const res = filterVal.map(j => v[j])
                    data_list.push(res)
                });
                return data_list
            },
            //处理时间格式
            dateFormat(row, column){
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
            },
            // 导入excel
            importExcel() {
                if(this.$refs.uploadExcel.uploadFiles.length===0){
                    this.$message.error("请选取文件")
                }else{
                    this.$refs.uploadExcel.submit();
                }
            },
            uploadSuccess(){
                this.$refs.uploadExcel.clearFiles();
                this.getData();
                alert('上传成功！');
            },
            handleError(err){
                alert(err)
            },
            // 查询标签数据
            querylabel() {
                this.$http.get(`asset/api/tag/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.labelData = res.data
                });
            },
            queryStaff() {
                this.$http.get(`asset/api/staff/`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.assetStaffData = res.data;
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 修改维护状态
            handlemaintain(row) {
                if(row.maintain_status == '是'){
                    row.maintain_status = "否"
                }else{
                    row.maintain_status = "是"
                }
                this.$http.put(`asset/api/virtual_server/${row.id}/update_maintain_state/`,row,{
                    headers:{
                        'token': localStorage.getItem('token')}
                }).then((res) => {
                    console.log('Response:' + JSON.stringify(res));
                    this.$message.success('状态修改成功');
                    this.getData()
                }).catch(function(error){
                    console.log(error.response.data)
                    alert(JSON.stringify(error.response.data))
                })
            },
        },
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .red {
        color: #ff0000;
    }

    .handle-box {
        margin-bottom: 20px;
    }

    .handle-input {
        width: 200px;
        display: inline-block;
    }
    .table-width {
        word-break: keep-all;
        white-space: nowrap;
    }
    .margin_bot{
        margin-bottom: 10px;
    }


</style>
