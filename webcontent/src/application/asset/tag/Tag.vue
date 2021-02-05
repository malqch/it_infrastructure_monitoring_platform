<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 标签
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="form">
                <el-row type="flex" class="row-bg" justify="space-between">
                    <div>
                        <el-button
                                type="primary"
                                icon="el-icon-edit"
                                @click="handleCreate()"
                                class="handle-box-1"
                        >增加
                        </el-button>
                    </div>
                    <div type="flex" class="row-bg" justify="end">
                        <el-form-item>
                            <el-input v-model="searchData.tag_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    :data="tableData"
                    border
                    class="table"
                    ref="multipleTable"
                    header-cell-class-name="table-header"
                    @selection-change="handleSelectionChange"
            >
<!--                <el-table-column type="selection"  align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="tag_name" label="标签名称" align="center"></el-table-column>
                <el-table-column prop="tag_remark" label="备注" align="center"></el-table-column>
                <el-table-column prop="create_time" :formatter="dateFormat" label="创建时间" align="center"></el-table-column>
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
            <el-form ref="editform" :rules="rules" :model="editform" label-width="70px">
                <el-form-item label="名称" prop="tag_name">
                    <el-input v-model="editform.tag_name"></el-input>
                </el-form-item>
                <el-form-item label="备注" prop="tag_remark">
                    <el-input type="textarea" v-model="editform.tag_remark" :value_data="aa" id="ID"></el-input>
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
                <el-form-item label="名称" prop="tag_name">
                    <el-input v-model="form.tag_name"></el-input>
                </el-form-item>
                <el-form-item label="备注" prop="tag_remark">
                    <el-input type="textarea" v-model="form.tag_remark"></el-input>
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
        name: 'tagtable',
        data() {
            return {
                aa: '1111',
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
                pageTotal: 0,
                form: {},
                editform: {},
                idx: -1,
                id: -1,

                searchData: {
                    tag_name: '',
                    is_delete: 0
                },
                rules: {
                    tag_name: [
                        {required: true, message: '请输入标签名', trigger: 'blur'}
                    ],
                    tag_remark: [
                        {required: true, message: '请输入标签名', trigger: 'blur'}
                    ]
                }
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`asset/api/tag/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&tag_name=${this.searchData.tag_name}&is_delete=${this.searchData.is_delete}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch( (error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
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
                this.$http.post(`asset/api/tag/`,
                    { 'tag_name': this.form.tag_name, 'tag_remark': this.form.tag_remark,
                        'create_time': this.form.create_time, 'remove_time': this.form.remove_time
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
                            tag_name: '',
                                is_delete: 0
                        };
                        this.getData()
                    } else {
                        this.$message.error('创建失败！');
                        this.form = {}
                    }
                }).catch( (error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
                });
                }).catch( (error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
                    this.$message.error('参数错误');
                });
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
                    tag_name: '',
                    is_delete: 0
                };
                this.getData();
            },

            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.put(`asset/api/tag/${row.id}/logic_delete/`,
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
                    console.log('Error' + error.response);
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
                    // console.log(this.$refs.getAttribute.value_data, 88888)
                    let inputObj = document.getElementById("ID").getAttribute('value_data');
                    // inputObj.getAttribute = ("value_data");
                    console.log(inputObj)
                    this.$http.put(`asset/api/tag/${this.id}/`,
                        { 'tag_name': this.editform.tag_name, 'tag_remark': this.editform.tag_remark},
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        console.log('Response:' + JSON.stringify(res));
                        if (res.status === 200) {
                            this.$message.success('修改成功！');
                            this.editVisible = false;
                            this.getData()
                        } else {
                            this.$message.error(res.data.msg);
                            this.getData()
                        }
                    }).catch( (error) => {
                        console.log('Error' + error.response);
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

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 200px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 12px;
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
