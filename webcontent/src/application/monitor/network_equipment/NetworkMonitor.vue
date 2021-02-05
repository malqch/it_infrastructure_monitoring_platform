<template>
    <div>
        <div class="wrapper">
            <!--<div class="crumbs">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>
                        <i class="el-icon-lx-cascades"></i> 网络设备监控项管理
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div>-->
            <div class="container">
                <el-form :inline="true" v-model="form">
                    <el-row type="flex" class="row-bg" justify="space-around">
                        <el-col :span="6">
                            <el-button
                                    type="primary"
                                    icon="el-icon-circle-plus-outline"
                                    @click="handleCreate()"
                                    class="handle-box-1"
                            >增加
                            </el-button>
                        </el-col>
                        <el-col :span="20" :inline="true">
                            <el-form-item>
                                <el-input v-model="searchData.indicator_name" clearable placeholder="指标名" class="handle-input"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="searchData.indicator_code" clearable placeholder="指标" class="handle-input"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="searchData.series_name" clearable placeholder="系列" class="handle-input"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="searchData.indicator_oid" clearable placeholder="标识符" class="handle-input"></el-input>
                            </el-form-item>
                            <el-button icon="el-icon-search" type="primary" class="handle-box change_el_button" @click="handleSearch">查询</el-button>
                        </el-col>
                    </el-row>
                </el-form>
                <!--            <div class="container">-->
                <!--                <el-input v-model="search" style="display: inline-block;width: 1300px"-->
                <!--                          placeholder="请输入搜索标识符">-->
                <!--                </el-input>-->
                <!--                <div style="display: inline-block">-->
                <!--                    <el-button-->
                <!--                            type="primary"-->
                <!--                            icon="el-icon-search"-->
                <!--                            @click="fuzzysearch()"-->
                <!--                            class="handle-box-1"-->
                <!--                    >搜索-->
                <!--                    </el-button>-->
                <!--                </div>-->
                <!--            </div>-->
                <el-table
                        :data="tableData"
                        border
                        style="width: 100%">
                    <el-table-column prop="id" label="序号" align="center"></el-table-column>
                    <el-table-column prop="indicator_name" label="指标名" align="center"></el-table-column>
                    <el-table-column prop="indicator_code" label="指标" align="center"></el-table-column>
                    <el-table-column prop="indicator_oid" label="指标标识" align="center"></el-table-column>
                    <el-table-column prop="series_name" label="系列" align="center"></el-table-column>
                    <el-table-column prop="gmt_create" :formatter="dateFormat" label="创建时间" align="center"></el-table-column>
                    <el-table-column prop="gmt_modified" :formatter="dateFormat" label="更新时间" align="center"></el-table-column>
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
                                    class="danger"
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
                <el-form ref="form" :model="edit_form" label-width="70px">
                    <el-form-item label="指标名">
                        <el-input v-model="edit_form.indicator_name"></el-input>
                    </el-form-item>
                    <el-form-item label="指标">
                        <el-input v-model="edit_form.indicator_code"></el-input>
                    </el-form-item>
                    <el-form-item label="标识符">
                        <el-input v-model="edit_form.indicator_oid"></el-input>
                    </el-form-item>
                    <el-form-item label="指标类型">
                        <el-select style="width:100%" value-key="id"  v-model="edit_form.indicator_type" :popper-append-to-body="false">
                            <el-option label="私有" value="1"></el-option>
                            <el-option label="共有" value="0"></el-option>
                        </el-select>
                        <!--                    <el-input v-model="edit_form.indicator_type"></el-input>-->
                    </el-form-item>
                    <el-form-item label="收集方式">

                        <el-input v-model="edit_form.collect_type"></el-input>
                    </el-form-item>
                    <el-form-item label="是否使用">
                        <el-select style="width:100%" value-key="id"  v-model="edit_form.is_active" placeholder="是否使用" :popper-append-to-body="false">
                            <!--                        <el-option v-for="item in activeData"-->
                            <!--                                   :key=item-->
                            <!--                                   :label="item"-->
                            <!--                                   :value=item>-->
                            <!--                        </el-option>-->
                            <el-option label="使用" value="1"></el-option>
                            <el-option label="禁用" value="0"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="系列">
                        <el-select style="width:100%" value-key="id"  v-model="edit_form.series_name" placeholder="请选择" @focus="queryseries()" :popper-append-to-body="false">
                            <el-option v-for="item in seriesData"
                                       :key=item.id
                                       :label="item.series_name"
                                       :value=item.id>
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetedit" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
            </el-dialog>
            <!-- 新增弹出框 -->
            <el-dialog title="创建" :visible.sync="createVisible" width="30%">
                <el-form ref="form" :model="form" label-width="70px">
                    <el-form-item label="指标名">
                        <el-input v-model="form.indicator_name"></el-input>
                    </el-form-item>
                    <el-form-item label="指标">
                        <el-input v-model="form.indicator_code"></el-input>
                    </el-form-item>
                    <el-form-item label="标识符">
                        <el-input v-model="form.indicator_oid"></el-input>
                    </el-form-item>
                    <el-form-item label="指标类型">
                        <el-input v-model="form.indicator_type"></el-input>
                    </el-form-item>
                    <el-form-item label="收集方式">
                        <el-input v-model="form.collect_type"></el-input>
                    </el-form-item>
                    <el-form-item label="是否使用">
                        <el-select style="width:100%" value-key="id"  v-model="form.is_active" placeholder="是否使用" :popper-append-to-body="false">
                            <el-option v-for="item in activeData"
                                       :key=item
                                       :label="item"
                                       :value=item>
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="系列">
                        <el-select style="width:100%" value-key="id"  v-model="form.series_id" placeholder="请选择" @focus="queryseries()" :popper-append-to-body="false">
                            <el-option v-for="item in seriesData"
                                       :key=item.id
                                       :label="item.series_name"
                                       :value=item.id>
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetCreate" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NetworkMonitor",
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
                pageTotal: 0,
                edit_form:{},
                form: {},
                idx: -1,
                id: -1,
                searchData: {
                    indicator_name: '',
                    indicator_code: '',
                    series_name: '',
                    indicator_oid: '',
                    is_delete: 0
                },
                activeData: ['使用', '禁用'],
                seriesData: [],
                search: "",
            };
        },
        created() {
            this.getData();
        },
        //
        // computed: {
        //     // 模糊搜索
        //     tables() {
        //         const search = this.search
        //         if (search) {
        //             // filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。
        //             // 注意： filter() 不会对空数组进行检测。
        //             // 注意： filter() 不会改变原始数组。
        //             return this.tableData.filter(data => {
        //                 // some() 方法用于检测数组中的元素是否满足指定条件;
        //                 // some() 方法会依次执行数组的每个元素：
        //                 // 如果有一个元素满足条件，则表达式返回true , 剩余的元素不会再执行检测;
        //                 // 如果没有满足条件的元素，则返回false。
        //                 // 注意： some() 不会对空数组进行检测。
        //                 // 注意： some() 不会改变原始数组。
        //                 return Object.keys(data).some(key => {
        //                     // indexOf() 返回某个指定的字符在某个字符串中首次出现的位置，如果没有找到就返回-1；
        //                     // 该方法对大小写敏感！所以之前需要toLowerCase()方法将所有查询到内容变为小写。
        //                     return String(data[key]).toLowerCase().indexOf(search) > -1
        //                 })
        //             })
        //         }
        //         return this.dormitory
        //     },
        // },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`monitor/api/network_monitor/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&indicator_name=${this.searchData.indicator_name}&indicator_code=${
                    this.searchData.indicator_code}&series_name=${this.searchData.series_name}&indicator_oid=${
                    this.searchData.indicator_oid}&is_delete=${this.searchData.is_delete}`, {
                    headers: {
                        'token':localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },

            // // 模糊查询
            // fuzzysearch() {
            //     this.getData();
            //     let _search = this.search;
            //     let newtableData = [];
            //     if (_search) {
            //         newtableData = this.tableData.filter(item => item.indicator_oid.match(_search))
            //         // this.tableData.filter(item => {
            //         //     console.log(item)
            //         //     if (item.indicator_oid.indexOf(_search) !== -1) {
            //         //         newtableData.push(item);
            //         //     }
            //         // })
            //     }
            //     console.log(newtableData)
            //     this.tableData = newtableData
            // },

            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },

            //查询业务信息
            queryseries() {
                this.$http.get(`monitor/api/series/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    console.log(res)
                    this.seriesData = res.data
                    console.log(this.seriesData)
                })
            },
            // 创建操作
            handleCreate() {
                this.createVisible = true;
            },
            // 保存创建
            saveCreate() {
                this.$http.post(`monitor/api/network_monitor/`,
                    { 'indicator_name': this.form.indicator_name, 'indicator_code': this.form.indicator_code,
                        'indicator_oid': this.form.indicator_oid, 'indicator_type': this.form.indicator_type,
                        'series_id': this.form.series_id, 'is_active': this.form.is_active, 'collect_type': this.form.collect_type,
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
                    } else {
                        this.$message.error('创建失败！');
                        this.form = {}
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
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
                    indicator_name: '',
                    indicator_code: '',
                    series_name: '',
                    indicator_oid: '',
                    is_delete: 0
                };
                this.getData();
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning',
                    customClass: 'message-logout',
                    cancelButtonClass:'change_el_button'
                }).then(() => {this.$http.put(`monitor/api/network_monitor/${row.id}/logic_delete/`,
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
            handleEdit(row) {
                this.id = row.id;
                this.edit_form = row;
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                this.$http.put(`monitor/api/network_monitor/${this.id}/`,
                    { 'indicator_name': this.edit_form.indicator_name, 'indicator_code': this.edit_form.indicator_code,
                        'indicator_oid': this.edit_form.indicator_oid, 'indicator_type': this.edit_form.indicator_type, 'is_active':
                        this.edit_form.is_active, 'series_id': this.edit_form.series_id, 'collect_type': this.edit_form.collect_type },
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
                        this.$message.error('修改失败！');
                        this.getData()
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
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
    @import "../../../assets/scss/serve";
    @import "../../../assets/scss/darkStyle";
</style>
<style>
    .message-logout{
        background-color:#24273e;
        border: 1px solid #3c4163;
        color:#fff;
    }
    .el-message-box__title{
        color:#409EFF;
    }
    .el-message-box__content{
        color:#fff;
    }
    .change_el_button{
        background: #2a2e49;
        border: 1px solid #2f3561;
        color:#fff;
    }
</style>