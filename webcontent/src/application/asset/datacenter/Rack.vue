<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 机柜
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
                                class="handle-box"
                        >增加
                        </el-button>
                    </div>
                    <div type="flex" class="row-bg" justify="end">
                        <el-form-item>
                            <el-input v-model="searchData.rack_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                                <el-input v-model="searchData.rack_address" clearable placeholder="位置" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.room_name" clearable placeholder="所属机房" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
            >
                <el-table-column  type="index" label="序号" align="center"></el-table-column>
                <el-table-column  prop="rack_name" align="center" label="名称"></el-table-column>
                <el-table-column  prop="rack_address" align="center" label="位置"></el-table-column>
                <el-table-column  prop="room_name" align="center" label="所属机房"></el-table-column>
                <el-table-column  prop="dc_name" align="center" label="所属数据中心"></el-table-column>
                <el-table-column  prop="remark" align="center" label="备注"></el-table-column>
                <el-table-column  prop="create_time" align="center" :formatter="dateFormat" label="创建时间"></el-table-column>
<!--                <el-table-column  prop="remove_time" align="center" label="移除时间"></el-table-column>-->
                <el-table-column prop="update_time" :formatter="dateFormat" label="更新时间" align="center"></el-table-column>
                <el-table-column fixed="right" label="操作" align="center">
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
                                @click="handleDelete(scope.row)"
                        >删除
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

        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
            <el-form ref="edit_form" :rules="rules" :model="edit_form" label-width="120px">
                <el-form-item label="名称" prop="rack_name">
                    <el-input v-model="edit_form.rack_name"></el-input>
                </el-form-item>
                <el-form-item label="位置" prop="rack_address">
                    <el-input v-model="edit_form.rack_address"></el-input>
                </el-form-item>
                <el-form-item label="所属数据中心" prop="dc_name">
                    <el-select style="width:100%" value-key="id"
                               v-model="edit_form.dc_name"
                               placeholder="请选择所属数据中心"
                               @focus="querydatacenter" >
                        <el-option v-for="item in datacenterData"
                                   :key=item.dc_name
                                   :label="item.dc_name"
                                   :value=item.dc_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="所属机房" prop="room_name">
                    <el-select style="width:100%" value-key="id"  v-model="edit_form.room_name" @focus="editqueryroom()" >
                        <el-option v-for="item in roomData"
                                   :key=item.room_name
                                   :label="item.room_name"
                                   :value=item.room_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="edit_form.remark"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetedit">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 新增弹出框 -->
        <el-dialog title="创建" :visible.sync="createVisible" width="30%">
            <el-form ref="form" :rules="rules" :model="form" label-width="120px">
                <el-form-item label="名称" prop="rack_name">
                    <el-input v-model="form.rack_name"></el-input>
                </el-form-item>
                <el-form-item label="位置" prop="rack_address">
                    <el-input v-model="form.rack_address"></el-input>
                </el-form-item>
                <el-form-item label="所属数据中心" prop="dc_name">
                    <el-select style="width:100%" value-key="id"
                               v-model="form.dc_name"
                               placeholder="请选择所属数据中心"
                               @focus="querydatacenter" >
                        <el-option v-for="item in datacenterData"
                                   :key=item.dc_name
                                   :label="item.dc_name"
                                   :value=item.dc_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="所属机房" prop="room_name">
                    <el-select style="width:100%" value-key="id"  v-model="form.room_name" placeholder="请选择所属机房" @focus="addqueryroom()" >
                        <el-option v-for="item in roomData"
                                   :key=item.room_name
                                   :label="item.room_name"
                                   :value=item.room_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.remark"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetCreate">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'racktable',
        data() {
            return {
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                datacenterData: [],
                roomData: [],
                rackData: [],
                multipleSelection: [],
                delList: [],
                editVisible: false,
                createVisible: false,
                pageTotal: 0,
                edit_form: {
                    dc_name: '',
                    room_id:'',
                    room_name:''
                },
                form: {
                    dc_name: '',
                    room_name: ''
                },
                idx: -1,
                id: -1,

                searchData: {
                    rack_name: '',
                    rack_address:'',
                    room_name: '',
                    // dc_name: '',
                    is_delete: 0
                },
                rules: {
                    rack_name: [
                        {required: true, message: '请输入机柜名称'},
                        {trigger: 'blur'}
                    ],
                    rack_address: [
                        {required: true, message: '请输入机柜地址'},
                        {trigger: 'blur'}
                    ],
                    dc_name: [
                        {required: true, message: '请选择数据中心'},
                        {trigger: 'blur'}
                    ],
                    room_name: [
                        {required: true, message: '请选择机房'},
                        {trigger: 'blur'}
                    ]
                },
                loading: true
            }
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`asset/api/rack/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&rack_name=${this.searchData.rack_name}&room_name=${
                    this.searchData.room_name}&rack_address=${this.searchData.rack_address}&is_delete=${
                    this.searchData.is_delete}`,
                    {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                    this.loading = false
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false
                });
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 创建操作
            handleCreate() {
                this.createVisible = true;
                this.form = {
                    dc_name: ""
                };
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存创建
            saveCreate() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$http.post(`asset/api/rack/`,
                        { 'rack_name': this.form.rack_name, 'rack_address': this.form.rack_address,
                            'remark': this.form.remark, 'room_name': this.form.room_name
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
                            this.getData()
                        } else if (res.status === 409){
                            this.$message.error['msg'];
                            this.createVisible = false;
                            this.form = {};
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

            // 重置编辑
            resetedit() {
                this.getData();
                this.editVisible = false
            },
            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.form = {
                    dc_name: ""
                };
            },
            // 保存删除操作
            saveDelete(row) {
                this.$http.put(`asset/api/rack/${row.id}/logic_delete/`,
                    {'is_delete': 1},
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

                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },

            //查询业务信息
            querydatacenter() {
                this.$set(this.form, "room_name", '')
                this.$set(this.edit_form, 'room_name', '')
                this.$http.get(`asset/api/datacenter/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.datacenterData = res.data;
                })
            },

            //修改时查询业务信息
            editqueryroom() {
                this.$http.get(`asset/api/room/?dc_name=${this.edit_form.dc_name}`,
                    {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    console.log(res)
                    this.roomData = res.data
                    console.log(this.roomData,111)
                })
            },
            //新增时查询业务信息
            addqueryroom() {
                if (this.form.dc_name === '') {
                    const datacenter = '未知'
                    this.$http.get(`asset/api/room/?dc_name=${datacenter}`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.roomData = res.data;
                })} else {
                this.$http.get(`asset/api/room/?dc_name=${this.form.dc_name}`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                    this.roomData = res.data;
                })
                console.log(222)
            }},
            // 删除操作
            handleDelete(row) {
                // 二次确认删除
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                })
                    .then(() => {
                        this.saveDelete(row)
                        this.tableData.splice(row, 1);
                    })
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
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.edit_form = row;
                console.log(row,111222)
                this.editVisible = true;
                this.edit_form.dc_name = row.dc_name;
                this.edit_form.room_name = row.room_name
                this.$http.get(`asset/api/rack/?id=${this.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        console.log(res)
                        this.rackData = res.data
                        console.log(this.rackData)
                })
                this.$nextTick(()=>{
                    this.$refs.edit_form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.edit_form.validate().then(res => {
                    console.log(res)
                    this.$http.put(`asset/api/rack/${this.id}/`,
                        { 'rack_name': this.edit_form.rack_name, 'rack_address': this.edit_form.rack_address,
                            'remark': this.edit_form.remark, 'room_name': this.edit_form.room_name
                        },
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            console.log(res,1123)
                            if (res.status === 200) {
                            this.$message.success('修改成功！');
                            this.editVisible = false;
                            this.getData()
                            }
                        }).catch(error=>{
                            console.log(1999);
                            this.editVisible = false;
                            this.getData();
                            if (error.response.status==409) {
                                console.log(error.response,1888)
                                console.log(JSON.parse(error.response.data).msg,1888)

                                this.$message.error(JSON.parse(error.response.data).msg);
                            }else{
                                this.$message.error(JSON.stringify(error.response.data));
                            }
                        })
                })
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
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
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 170px;
        display: inline-block;
    }
    .red {
        color: #ff0000;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }
    .handle-box {
        margin-bottom: 20px;
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
