<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 巡检任务
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="form">
                <el-row type="flex" class="row-bg" justify="space-between">
                    <div>
                        <el-button
                                type="primary"
                                icon="el-icon-circle-plus-outline"
                                @click="handleCreate()"
                                class="handle-box-1"
                        >新增
                        </el-button>
                    </div>
                    <div type="flex" class="row-bg" justify="end">
                        <el-form-item>
                            <el-input v-model="searchData.patrol_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    :data="tableData"
                    border
                    tooltip-effect="dark"
                    style="width: 100%; cursor:pointer"
                    max-height="600"
            >
                        <el-table-column prop="patrol_name" label="巡检任务名称" align="center"></el-table-column>
                        <el-table-column prop="start_time" label="开始时间" :formatter="dateFormat" align="center"></el-table-column>
                        <el-table-column prop="end_time" label="结束时间" :formatter="dateFormat" align="center"></el-table-column>
                        <el-table-column prop="script" label="脚本信息" align="center">
                            <template slot-scope="scope">
                                <el-link type="info" @click="searchScript(scope.row)" class="color-link">查看脚本信息</el-link>
                            </template>
                        </el-table-column>
                        <el-table-column prop="params" label="参数" align="center" ></el-table-column>
                        <el-table-column prop="exec_time" label="脚本执行时间" align="center" ></el-table-column>
                        <el-table-column prop="period" label="周期" align="center"></el-table-column>
                        <el-table-column prop="status" label="状态" align="center"></el-table-column>
                        <el-table-column prop="create_time" label="创建时间" :formatter="dateFormat" align="center" ></el-table-column>
                        <el-table-column prop="update_time" label="更新时间" :formatter="dateFormat" align="center"></el-table-column>
                        <el-table-column label="操作" width="270px" align="center">
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
                                        style="color: red"
                                        @click="handleDelete(scope.row)"
                                >删除
                                </el-button>
                                <el-button
                                        v-if="scope.row.status === '执行中'"
                                        type="text"
                                        icon="el-icon-video-pause"
                                        class="color-link"
                                        @click="handlestopPatrol(scope.row)"
                                >停止
                                </el-button>
                                <el-button
                                        v-if="scope.row.status === '已暂停'"
                                        type="text"
                                        icon="el-icon-video-play"
                                        class="color-green"
                                        @click="handleResume(scope.row)"
                                >重启
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
        <!-- 新增-->
        <el-dialog title="创建" :visible.sync="createVisible" width="30%">
            <el-form ref="form" :model="form" label-width="70px">
                <el-form-item label="巡检任务名称" prop="patrol_name">
                    <el-input v-model="form.patrol_name"></el-input>
                </el-form-item>
                <el-form-item label="开始时间" prop="start_time">
                    <el-date-picker
                            v-model="form.start_time"
                            type="datetime"
                            placeholder="选择日期"
                            style="width: 100%">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="结束时间" prop="end_time">
                    <el-date-picker
                            v-model="form.end_time"
                            type="datetime"
                            placeholder="选择日期"
                            style="width: 100%">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="选择脚本" prop="script">
                    <el-select multiple style="width:100%" v-model="form.script" placeholder="请选择脚本" @focus="addqueryscript" >
                        <el-option v-for="item in scriptData"
                                   :key=item.id
                                   :label=item.script_name
                                   :value=item.id>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="巡检周期" prop="period">
                    <el-select style="width:100%" v-model="form.period" placeholder="请选择脚本" @focus="addqueryscript" >
                        <el-option v-for="item in period_options"
                                   :key=item.value
                                   :label=item.label
                                   :value=item.value>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="参数" prop="params">
                    <el-input v-model="form.params"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetCreate">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
        </el-dialog>

        <!--编辑-->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="edit_form" :model="edit_form" label-width="70px">
                <el-form-item label="巡检任务名称" prop="patrol_name">
                    <el-input v-model="edit_form.patrol_name"></el-input>
                </el-form-item>
                <el-form-item label="开始时间" prop="start_time">
                    <el-date-picker
                            v-model="edit_form.start_time"
                            type="datetime"
                            placeholder="选择日期"
                            style="width: 100%">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="结束时间" prop="end_time">
                    <el-date-picker
                            v-model="edit_form.end_time"
                            type="datetime"
                            placeholder="选择日期"
                            style="width: 100%">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="选择脚本" prop="script">
<!--                    <el-select-->
<!--                            v-model="edit_form.script"-->
<!--                            clearable-->
<!--                            filterable-->
<!--                            remote-->
<!--                            multiple-->
<!--                            :remote-method="queryscript"-->
<!--                            placeholder="脚本"-->
<!--                            style="width: 100%"-->
<!--                            class="handle-input mr10"-->
<!--                            :popper-append-to-body="false">-->
<!--                        <el-option-->
<!--                                v-for="(domain) in scriptData"-->
<!--                                :key="domain.id"-->
<!--                                :disabled="domain.disabled"-->
<!--                                :label="domain.script_name"-->
<!--                                :value="domain.id">-->
<!--                        </el-option>-->
<!--                    </el-select>-->
                    <el-select multiple style="width:100%" v-model="edit_form.script" placeholder="请选择脚本" @change="queryscript" >
                        <el-option v-for="item in scriptData"
                                   :key=item.id
                                   :disabled="item.disabled"
                                   :label="item.script_name"
                                   :value=item.id>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="巡检周期" prop="period">
                    <el-input v-model="edit_form.period"></el-input>
                </el-form-item>
                <el-form-item label="参数" prop="params">
                    <el-input v-model="edit_form.params"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetEdit">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!--脚本信息弹出框-->
        <el-dialog title="脚本信息" :visible.sync="scriptVisible" width="30%" class="alert_dialog">
            <ul :model="queryscriptData" v-for="item in queryscriptData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">脚本名称:</label>
                    <span class="network_span">{{item.script_name}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">脚本类型:</label>
                    <span class="network_span">{{item.script_type}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">分类:</label>
                    <span class="network_span">{{item.category}}
                    </span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">测试状态:</label>
                    <span class="network_span">{{item.test_status}}</span>
                </li>
            </ul>
        </el-dialog>

        <!-- 暂停弹出框 -->
        <el-dialog title="提示" :visible.sync="pauseVisible" width="25%">
            <span>确定暂停定时任务 {{uuid}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="pauseVisible = false">取 消</el-button>
                <el-button type="primary" @click="stopPatrol">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 重启弹出框 -->
        <el-dialog title="提示" :visible.sync="resumeVisible" width="25%">
            <span>确定重启定时任务 {{uuid}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resumeVisible = false">取 消</el-button>
                <el-button type="primary" @click="resumeTimedTask">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "HostGroup",
        data() {
            return {
                query: {
                    patrol_name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                pageTotal: 0,
                tableData: [], // 查询返回的数据
                queryscriptData: [], // 查询返回的脚本相关的信息
                scriptData: [],  // 脚本信息
                searchData: {
                    patrol_name: '',
                    is_delete: 0
                },
                createVisible: false,
                editVisible: false,
                scriptVisible: false,
                pauseVisible: false,
                resumeVisible: false,
                uuid: '',
                patrol_id: '',
                form: {},
                edit_form: {},
                rules: {
                    patrol_name: [
                        {required: true, message: '请输入巡检任务名称'},
                        {trigger: 'blur'}
                    ],
                    period: [
                        {required: true, message: '请输入巡检周期'},
                        {trigger: 'blur'}
                    ]
                },
                period_options: [
                    {
                        value: 'day',
                        label: '按天执行'
                    }
                ],
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.$http.get(`automation/api/patrol/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&patrol_name=${this.searchData.patrol_name}&is_delete=${this.searchData.is_delete}`,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        console.log(res.data['data'],111)
                    console.log(res.status,222)
                    if(res){
                        this.tableData = res.data['data'];
                        this.pageTotal = res.data.total_count;
                    }
                })
            },

            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.form = {};
                this.searchData = {
                    patrol_name: '',
                };
                this.getData();
            },

            // 创建操作
            handleCreate() {
                this.createVisible = true;
            },

            // 保存创建
            saveCreate() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$http.post(`automation/api/patrol/`,
                        { 'patrol_name': this.form.patrol_name, 'start_time': this.form.start_time, 'script': this.form.script,
                            'end_time': this.form.end_time, 'period': this.form.period, 'params': this.form.params
                        },
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 201) {
                            this.$message.success('创建成功！');
                            this.createVisible = false;
                            this.form = {};
                            this.searchData = {
                                patrol_name: '',
                            }
                            this.getData()
                        } else {
                            this.$message.error('创建失败！');
                            this.form = {}
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },

            handleSearchHost() {
                this.$set(this.query, 'pageIndex', 1);
                this.getNetwork();
            },

            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.edit_form = row;
                this.$http.get('automation/api/script/?use=1',
                    {
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res)=>{
                    this.scriptData = res.data;
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
                for (let i in this.edit_form.script) {
                    for (let j in this.scriptData) {
                        if (this.edit_form.script[i] === this.scriptData[j].id) {
                            this.edit_form.script[i] = this.scriptData[j].script_name
                        }
                    }
                }
                this.scriptData = [];
                this.editVisible = true;
            },

            //重置编辑
            resetEdit(){
                this.editVisible = false;
                this.edit_form = {};
                this.searchData = {
                    patrol_name: '',
                };
                this.getData();
            },

            // 保存编辑
            saveEdit() {
                this.$refs.edit_form.validate().then(res => {
                    console.log(res)
                    this.$http.put(`automation/api/patrol/${this.id}/`,
                        { 'patrol_name': this.edit_form.patrol_name, 'start_time': this.edit_form.start_time,
                            'script': this.edit_form.script, 'end_time': this.edit_form.end_time,
                            'period': this.edit_form.period, 'params': this.edit_form.params },
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 200) {
                            this.$message.success('修改成功！');
                            this.editVisible = false;
                            this.getData()
                        } else {
                            this.editVisible = false;
                            this.$message.error('修改失败！');
                            this.getData()
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },

            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.post(`automation/api/script/remove_timed_task/`,
                    {'uuid': row.uuid, 'id': row.id},
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    if (res.status === 200) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    } else {
                        this.$message.error(res.data.msg);
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    }

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},

            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },

            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            delAllSelection() {
                const length = this.multipleSelection.length;
                let str = '';
                this.delList = this.delList.concat(this.multipleSelection);
                for (let i = 0; i < length; i++) {
                    str += this.multipleSelection[i].name + ' ';
                }
                this.$message.error(`删除了${str}`);
                this.multipleSelection = [];
            },

            // 查询脚本信息
            queryscript() {
                this.$http.get(`automation/api/script/?use=1`,
                    {headers: {
                    'token': localStorage.getItem('token')
                }}).then((res) => {
                    this.scriptData = res.data;
                })
                for (let i in this.edit_form.script) {
                    for (let j in this.scriptData) {
                        this.$set(this.scriptData[j], 'disabled', false)
                        if (this.edit_form.script[i] === this.scriptData[j].script_name) {
                            this.scriptData[j].disabled = true;
                        }
                    }
                }
            },

            addqueryscript() {
                this.$http.get(`automation/api/script/?use=1`,
                    {headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                    this.scriptData = res.data;
                })
            },


            searchScript(row) {
                this.$http.get(`automation/api/patrol/script/?id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.queryscriptData = res.data;
                    if(this.queryscriptData==""){
                        this.$message.warning("脚本信息不存在");
                    }else{
                        this.scriptVisible = true;
                        for(let item in this.queryscriptData) {
                            let scriptTime = new Date(this.queryscriptData[item].create_time).toJSON();
                            this.queryscriptData[item].create_time = new Date(
                                +new Date(scriptTime) + 8 * 3600 * 1000
                            )
                                .toISOString()
                                .replace(/T/g, " ")
                                .replace(/\.[\d]{3}Z/, "");

                        }
                    }
                });
            },

            //处理停止巡检任务
            handlestopPatrol(row) {
                this.uuid = row.uuid;
                this.patrol_id = row.id;
                this.pauseVisible = true;
            },

            // 停止巡检任务
            stopPatrol() {
                this.$http.post(`automation/api/script/pause_timed_task/`,
                    {'uuid': this.uuid, 'id': this.patrol_id},
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) =>{
                    if(res.status === 200) {
                        this.$message.success('暂停成功！');
                        this.pauseVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('暂停失败！');
                        this.pauseVisible = false;
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.pauseVisible = false;
                });
            },

            // 触发重启按钮
            handleResume(row) {
                if (new Date().getTime() < new Date(row.end_time).getTime()) {
                    this.uuid = row.uuid;
                    this.patrol_id = row.id;
                    this.resumeVisible = true;
                } else {
                    this.$message.error('重启失败！巡检任务结束时间已过!');
                }

            },
            // 重启定时任务
            resumeTimedTask() {
                this.$http.post(`automation/api/script/restart_timed_task/`,
                    {'uuid': this.uuid, 'id': this.patrol_id},
                    {
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('重启成功！');
                        this.resumeVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('重启失败！');
                        this.resumeVisible = false;
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.resumeVisible = false;
                });
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
        }
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
    .create-input {
        width: 260px;
    }
    .prompt-border {
        height: 130px;
        padding: 10px;
        border: 1px solid #c5c3c3
    }
    .trans_button_cls{
        text-align: center;
        margin-top: 15%;
    }
    .trans_table_cls{
        height: 200px;
        overflow: auto;
    }
</style>