<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 数据中心
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
                        >增加
                        </el-button>
                    </div>
                    <div type="flex" class="row-bg" justify="end">
                        <el-form-item>
                            <el-input v-model="searchData.dc_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.dc_address" clearable placeholder="地址" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="dc_name" label="数据中心名称" align="center"></el-table-column>
                <el-table-column prop="dc_address" label="地址" align="center"></el-table-column>
                <el-table-column prop="remark" label="备注" align="center"></el-table-column>
                <el-table-column prop="dc_room" label="机房信息" align="center">
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchRoom(scope.row)" class="color-link">查看机房信息</el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="create_time" :formatter="dateFormat" label="注册时间" align="center"></el-table-column>
                <el-table-column prop="update_time" :formatter="dateFormat" label="更新时间" align="center"></el-table-column>
                <el-table-column label="操作"  align="center">
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
            <el-form ref="edit_form" :rules="rules" :model="edit_form" label-width="70px">
                <el-form-item label="名称" prop="dc_name">
                    <el-input v-model="edit_form.dc_name"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop="dc_address">
                    <el-input v-model="edit_form.dc_address"></el-input>
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
            <el-form ref="form" :rules="rules" :model="form" label-width="70px">
                <el-form-item label="名称" prop="dc_name">
                    <el-input v-model="form.dc_name"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop="dc_address">
                    <el-input v-model="form.dc_address"></el-input>
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
        <!--机房信息弹出框-->
        <el-dialog title="机房信息" :visible.sync="roomVisible" width="30%" class="alert_dialog">
            <ul :model="queryroomData" v-for="item in queryroomData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">room_name:</label>
                    <span class="network_span">{{item.room_name}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">remark:</label>
                    <span class="network_span">{{item.remark}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">room_address:</label>
                    <span class="network_span">{{item.room_address}}
                    </span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">create_time:</label>
                    <span class="network_span">{{item.create_time}}</span>
                </li>
            </ul>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'datacentertable',
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
                editVisible: false,
                createVisible: false,
                roomVisible: false,
                pageTotal: 0,
                edit_form:{},
                form: {},
                idx: -1,
                id: -1,
                searchData: {
                    dc_name: '',
                    dc_address: '',
                    is_delete: 0
                },
                queryroomData: [{}],
                rules: {
                    dc_name: [
                        {required: true, message: '请输入数据中心名称'},
                        {trigger: 'blur'}
                    ],
                    dc_address: [
                        {required: true, message: '请输入地址'},
                        {trigger: 'blur'}
                    ]
                },
                loading: true
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`asset/api/datacenter/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&dc_name=${this.searchData.dc_name}&dc_address=${
                    this.searchData.dc_address}&is_delete=${this.searchData.is_delete}`, {
                    headers: {
                        'token':localStorage.getItem('token')
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
            searchRoom(row) {
                this.$http.get(`asset/api/room/room/?id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.queryroomData = res.data;
                    if(this.queryroomData==""){
                        this.$message.warning("机房信息不存在");
                    }else{
                        this.roomVisible = true;
                        for(let item in this.queryroomData) {
                            let roomTime = new Date(this.queryroomData[item].create_time).toJSON();
                            this.queryroomData[item].create_time = new Date(
                                +new Date(roomTime) + 8 * 3600 * 1000
                            )
                                .toISOString()
                                .replace(/T/g, " ")
                                .replace(/\.[\d]{3}Z/, "");

                        }
                    }
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
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存创建
            saveCreate() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$http.post(`asset/api/datacenter/`,
                        { 'dc_name': this.form.dc_name, 'dc_address': this.form.dc_address, 'remark': this.form.remark
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
                                dc_name: '',
                                dc_address: '',
                                is_delete: 0
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
            // 重置编辑
            resetedit() {
                this.getData();
                this.editVisible = false
            },

            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.form = {};
                this.searchData = {
                    dc_name: '',
                    dc_address: '',
                    is_delete: 0
                };
                this.getData();
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.put(`asset/api/datacenter/${row.id}/logic_delete/`,
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

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},
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
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.edit_form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.edit_form.validate().then(res => {
                    console.log(res)
                    this.$http.put(`asset/api/datacenter/${this.id}/`,
                        { 'dc_name': this.edit_form.dc_name, 'dc_address': this.edit_form.dc_address, 'remark': this.edit_form.remark },
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
        width: 300px;
        display: inline-block;
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
