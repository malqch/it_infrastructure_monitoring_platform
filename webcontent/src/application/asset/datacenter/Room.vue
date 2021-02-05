<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 机房
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
                            <el-input v-model="searchData.room_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.room_address" clearable placeholder="位置" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.dc_name" clearable placeholder="所属数据中心" class="handle-input"></el-input>
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
                <el-table-column  prop="room_name" align="center" label="名称"></el-table-column>
                <el-table-column  prop="room_address" align="center" label="位置"></el-table-column>
                <el-table-column  prop="dc_name" align="center" label="所属数据中心"></el-table-column>
                <el-table-column prop="dc_room" label="机柜信息" align="center">
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchRack(scope.row)" class="color-link">查看机柜信息</el-link>
                    </template>
                </el-table-column>
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
            <el-form ref="edit_form" :rules="editrules" :model="edit_form" label-width="120px">
                <el-form-item label="名称" prop="room_name">
                    <el-input v-model="edit_form.room_name"></el-input>
                </el-form-item>
                <el-form-item label="位置" prop="room_address">
                    <el-input v-model="edit_form.room_address"></el-input>
                </el-form-item>
                <el-form-item label="所属数据中心" prop="dc_name">
                    <el-select style="width:100%" v-model="edit_form.dc_name" placeholder="请选择所属数据中心" @focus="querydatacenter" @change="querydatacenter" >
                        <el-option v-for="item in datacenterData"
                                   :key=item.id
                                   :label="item.dc_name"
                                   :value=item.id>
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
            <el-form ref="form" :rules="addrules" :model="form" label-width="120px">
                <el-form-item label="名称" prop="room_name">
                    <el-input v-model="form.room_name"></el-input>
                </el-form-item>
                <el-form-item label="位置" prop="room_address">
                    <el-input v-model="form.room_address"></el-input>
                </el-form-item>
                <el-form-item label="所属数据中心" prop="datacenter_id">
                    <el-select style="width:100%" value-key="id"  v-model="form.datacenter_id" placeholder="请选择所属数据中心" @focus="querydatacenter()" >
                        <el-option v-for="item in datacenterData"
                                   :key=item.id
                                   :label="item.dc_name"
                                   :value=item.id>
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

        <!--机柜信息弹出框-->
        <el-dialog title="机柜信息" :visible.sync="rackVisible" width="35%">
            <ul :model="queryrackData" v-for="item in queryrackData" :key="item.rack_name" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">rack_name:</label>
                    <span class="network_span">{{item.rack_name}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">rack_address:</label>
                    <span class="network_span">{{item.rack_address}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">remark:</label>
                    <span class="network_span">{{item.remark}}
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
    import {isInteger} from '../../../util/validate'
    export default {
        name: 'roomtable',
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
                multipleSelection: [],
                delList: [],
                editVisible: false,
                createVisible: false,
                rackVisible: false,
                pageTotal: 0,
                edit_form: {
                    datacenter_id:'',
                    dc_name:''
                },
                form: {
                    datacenter_id:''
                },
                idx: -1,
                id: -1,

                searchData: {
                    room_name: '',
                    room_address:'',
                    dc_name: '',
                    is_delete: 0
                },
                queryrackData: [{}],
                addrules: {
                    room_name: [
                        {required: true, message: '请输入机房名称'},
                        {trigger: 'blur'}
                    ],
                    room_address: [
                        {required: true, message: '请输入机房地址'},
                        {trigger: 'blur'}
                    ],
                    datacenter_id: [
                        {required: true, message: '请选择数据中心'},
                        {validator: isInteger, trigger: 'blur'}
                    ]
                },
                editrules: {
                    room_name: [
                        {required: true, message: '请输入机房名称'},
                        {trigger: 'blur'}
                    ],
                    room_address: [
                        {required: true, message: '请输入机房地址'},
                        {trigger: 'blur'}
                    ],
                    datacenter: [
                        {required: true, message: '请选择数据中心'},
                        {validator: isInteger, trigger: 'blur'}
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
                this.$http.get(`asset/api/room/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&room_name=${this.searchData.room_name}&dc_name=${
                    this.searchData.dc_name}&room_address=${this.searchData.room_address}&is_delete=${this.searchData.is_delete}`, {
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

            searchRack(row) {
                this.$http.get(`asset/api/rack/rack/?room_id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.queryrackData = res.data;
                    if(this.queryrackData==""){
                        this.$message.warning("机柜信息不存在");
                    }else{
                        this.rackVisible = true;
                        for(let item in this.queryrackData) {
                            let rackTime = new Date(this.queryrackData[item].create_time).toJSON();
                            this.queryrackData[item].create_time = new Date(
                                +new Date(rackTime) + 8 * 3600 * 1000
                            )
                                .toISOString()
                                .replace(/T/g, " ")
                                .replace(/\.[\d]{3}Z/, "");

                        }
                    }
                });
            },

            //查询业务信息
            querydatacenter() {
                this.$http.get(`asset/api/datacenter/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.datacenterData = res.data
                })
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
                    this.$http.post(`asset/api/room/`,
                        { 'room_name': this.form.room_name, 'remark': this.form.remark, 'datacenter_id': this.form.datacenter_id,
                            'room_address': this.form.room_address
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
                                room_name: '',
                                room_address:'',
                                dc_name: '',
                                is_delete: 0
                            };
                            this.getData();
                        } else if (res.status === 409){
                            this.$message.error['msg'];
                            this.createVisible = false;
                            this.form = {};
                            this.searchData = {
                                room_name: '',
                                room_address:'',
                                dc_name: '',
                                is_delete: 0
                            };
                            this.getData();
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
                this.form = {}
            },
            // 保存删除操作
            saveDelete(row) {
                this.$http.put(`asset/api/room/${row.id}/logic_delete/`,
                    {'room_name': row.room_name, 'is_delete': 1},
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
            },

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
                this.editVisible = true;
                this.edit_form.dc_name = row.dc_name;
                this.$nextTick(()=>{
                    this.$refs.edit_form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                console.log(this.edit_form.datacenter,123)
                if(this.edit_form.dc_name && typeof this.edit_form.dc_name != "number"){
                    this.edit_form.datacenter_id = this.edit_form.datacenter.id
                } else {
                    this.edit_form.datacenter_id = this.edit_form.dc_name
                }
                this.$refs.edit_form.validate().then(res => {
                    console.log(res)
                    this.$http.put(`asset/api/room/${this.id}/`,
                        { 'room_name': this.edit_form.room_name, 'remark': this.edit_form.remark,
                            'room_address': this.edit_form.room_address, 'datacenter_id': this.edit_form.datacenter_id
                        },
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 200) {
                            this.$message.success('修改成功！');
                            this.editVisible = false;
                            this.getData()
                        } else if (res.status === 205){
                            this.$message.error('修改失败！');
                            this.getData()
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                        this.getData();
                        this.editVisible= false;
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
        width:180px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .handle-box {
        margin-bottom: 20px;
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
