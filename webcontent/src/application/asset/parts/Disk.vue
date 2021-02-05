<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 备件管理
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
                            <el-input v-model="searchData.disk_status" clearable placeholder="状态" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.disk_sn" clearable placeholder="SN" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.disk_vendor" clearable placeholder="厂商" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.disk_host" clearable placeholder="所属主机" class="handle-input"></el-input>
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
                <el-table-column  prop="disk_vendor" align="center" label="厂商"></el-table-column>
                <el-table-column  prop="disk_sn" align="center" label="SN"></el-table-column>
                <el-table-column  prop="disk_capacity" align="center" label="容量"></el-table-column>
                <el-table-column  prop="disk_status" align="center" label="状态"></el-table-column>
                <af-table-column  prop="disk_host" align="center" label="所属主机"></af-table-column>
                <af-table-column  prop="disk_service_start_time" align="center" label="服务开始时间"></af-table-column>
                <af-table-column  prop="disk_service_end_time" align="center" label="服务结束时间"></af-table-column>
                <af-table-column fixed="right" label="操作"  align="center" width="150">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
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
                </af-table-column>
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
            <el-form ref="editform" :rules="rules" :model="editform" label-width="100px">
                <el-form-item label="厂商" prop="disk_vendor">
                    <el-select style="width:100%" value-key="vendor_name"  v-model="editform.disk_vendor" placeholder="请选择所属厂商" @focus="queryvendor()" >
                        <el-option v-for="item in vendorData"
                                   :key=item.vendor_name
                                   :label="item.vendor_name"
                                   :value=item.vendor_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="SN" prop="disk_sn">
                    <el-input v-model="editform.disk_sn"></el-input>
                </el-form-item>
                <el-form-item label="容量">
                    <el-input type="number" v-model="editform.disk_capacity"></el-input>
                </el-form-item>
                <el-form-item label="状态">
                    <el-input v-model="editform.disk_status"></el-input>
                </el-form-item>
                <el-form-item label="所属主机">
                    <el-select style="width:100%" value-key="id" v-model="editform.disk_host"  filterable remote placeholder="请输入所属主机名称或ip" :remote-method="queryHost">
                        <el-option v-for="item in hostData"
                                   :key=item.id
                                   :label="`${item.hostname}/${item.device_ip}`"
                                   :value="`${item.hostname}/${item.device_ip}`">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="服务开始时间">
                    <el-date-picker
                            v-model="editform.disk_service_start_time"
                            type="date"
                            placeholder="选择日期"
                            :editable="false"
                            style="width: 100%"
                            value-format=yyyy-MM-dd>
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="服务结束时间">
                    <el-date-picker
                            v-model="editform.disk_service_end_time"
                            type="date"
                            placeholder="选择日期"
                            :editable="false"
                            style="width: 100%"
                            value-format=yyyy-MM-dd>
                    </el-date-picker>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetedit">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>

        <!-- 新增弹出框 -->
        <el-dialog title="创建" :visible.sync="createVisible" :show-close="false" width="30%">
            <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                <el-form-item label="厂商" prop="disk_vendor">
                    <el-select style="width:100%" value-key="vendor_name"  v-model="form.disk_vendor" placeholder="请选择所属厂商" @focus="queryvendor()" >
                        <el-option v-for="item in vendorData"
                                   :key=item.vendor_name
                                   :label="item.vendor_name"
                                   :value=item.vendor_name>
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="SN" prop="disk_sn">
                    <el-input v-model="form.disk_sn"></el-input>
                </el-form-item>
                <el-form-item label="容量">
                    <el-input type="number" v-model="form.disk_capacity"></el-input>
                </el-form-item>
                <el-form-item label="状态">
                    <el-input v-model="form.disk_status"></el-input>
<!--                    <el-input v-model="form.disk_status"></el-input>-->
                </el-form-item>
                <el-form-item label="所属主机">
                    <el-select style="width:100%" value-key="id" v-model="form.disk_host" filterable  remote placeholder="请输入所属主机名称或ip" :remote-method="queryHost">
                        <el-option v-for="item in hostData"
                                   :key=item.id
                                   :label="`${item.hostname}/${item.device_ip}`"
                                   :value="`${item.hostname}/${item.device_ip}`">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="服务开始时间">
                    <el-date-picker
                            v-model="form.disk_service_start_time"
                            type="date"
                            placeholder="选择日期"
                            :editable="false"
                            style="width: 100%"
                            value-format=yyyy-MM-dd>
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="服务结束时间">
                    <el-date-picker
                            v-model="form.disk_service_end_time"
                            type="date"
                            placeholder="选择日期"
                            :editable="false"
                            style="width: 100%"
                            value-format=yyyy-MM-dd>
                    </el-date-picker>
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
        name: 'disktable',
        data() {
            return {
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                vendorData: [],
                multipleSelection: [],
                delList: [],
                editVisible: false,
                createVisible: false,
                disk_vendor: "",
                pageTotal: 0,
                form: {"disk_capacity": 0},
                editform: {},
                idx: -1,
                id: -1,

                searchData: {
                    disk_vendor: '',
                    disk_host: '',
                    disk_sn: '',
                    disk_status: '',
                    'is_delete': 0
                },
                rules: {
                    disk_vendor: [
                        {required: true, message: "请输入厂商"},
                        {trigger: 'blur'}
                    ],
                    disk_sn: [
                        {required: true, message: '请输入sn'},
                        {trigger: 'blur'}
                    ],
                    disk_qn: [
                        {required: true, message: '请输入qn'},
                        {trigger: 'blur'}
                    ],
                },
                hostData: [], // 所属主机查询
                loading: true
            };

        },


        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get( `asset/api/disk/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&disk_status=${this.searchData.disk_status}&disk_sn=${
                    this.searchData.disk_sn}&disk_vendor=${this.searchData.disk_vendor}&disk_host=${
                    this.searchData.disk_host}&is_delete=${this.searchData.is_delete}`,
                    {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                    this.loading = false
                }).catch( (error)=>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false
                });
            },

            //查询业务信息
            queryvendor() {
                this.$http.get( `asset/api/vendor/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    console.log(res)
                    this.vendorData = res.data
                    console.log(this.vendorData)
                })
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },

            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.put( `asset/api/disk/${row.id}/logic_delete/`,
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
                        this.$message.error('删除失败！');
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
            handleEdit(index, row) {
                this.id = row.id;
                this.editform = row;
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.editform.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.editform.validate().then(res => {
                    console.log(res)
                    this.$http.put( `asset/api/disk/${this.id}/`,
                        { 'disk_vendor': this.editform.disk_vendor, 'disk_sn': this.editform.disk_sn, 'disk_capacity': this.editform.disk_capacity,
                            'disk_status': this.editform.disk_status, 'disk_host': this.editform.disk_host,
                            'disk_service_start_time': this.editform.disk_service_start_time, 'disk_service_end_time': this.editform.disk_service_end_time
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
                        } else {
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
            // 重置编辑
            resetedit() {
                this.getData();
                this.editVisible = false
            },
            // 新增操作
            handleCreate() {
                this.createVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存新增
            saveCreate() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$http.post( `asset/api/disk/`,
                        { 'disk_vendor': this.form.disk_vendor, 'disk_sn': this.form.disk_sn, 'disk_capacity': this.form.disk_capacity,
                            'disk_status': this.form.disk_status, 'disk_host': this.form.disk_host,
                            'disk_service_start_time': this.form.disk_service_start_time, 'disk_service_end_time': this.form.disk_service_end_time
                        },
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 201) {
                            this.$message.success('创建成功！');
                            this.createVisible = false;
                            this.form = {"disk_capacity": 0};
                            this.vendorData = [];
                            this.searchData = {
                                disk_vendor: '',
                                    disk_host: '',
                                    disk_sn: '',
                                    disk_status: '',
                                    'is_delete': 0
                            };
                            this.getData()
                        } else {
                            this.$message.error('创建失败！');
                            this.vendorData = [];
                            this.form = {"disk_capacity": 0}
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
            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.vendorData = [];
                this.form = {"disk_capacity": 0}
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
            // 查询主机信息
            queryHost(query){
                console.log(query,111)
                this.$http.get(`asset/api/device/device/?query=${query}`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.hostData = res.data;
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            }
        }
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve";
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
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
