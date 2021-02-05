<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row type="flex" class="row-bg" justify="space-between">
                <div>
                    <el-button
                            type="primary"
                            icon="el-icon-circle-plus-outline"
                            @click="handleCreate">新增</el-button>
                </div>
                <div>
                    <el-input
                            type="text"
                            placeholder="请输入脚本名"
                            v-model="keywords"
                            style="width:200px; margin-bottom:15px;"
                            clearable>
                    </el-input>
                    <el-button style="margin-left:10px;" type="primary" @click="handleSearch">查询</el-button>
                </div>
            </el-row>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="script_name" label="脚本名字" align="center"></el-table-column>
                <el-table-column prop="script_type" label="脚本类型" align="center"></el-table-column>
                <el-table-column prop="category" label="所属分类" align="center"></el-table-column>
                <el-table-column label="脚本内容" align="center">
                    <template slot-scope="scope_content">
                        <el-tooltip class="item" effect="dark" :content=scope_content.row.content placement="top-start">
                            <span>{{ scope_content.row.content }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="脚本说明" align="center">
                    <template slot-scope="scope_desc">
                        <el-tooltip class="item" effect="dark" :content=scope_desc.row.desc placement="top-start">
                            <span>{{ scope_desc.row.desc }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="脚本参数" align="center">
                    <template slot-scope="scope_param">
                        <el-tooltip class="item" effect="dark" :content=scope_param.row.param placement="top-start">
                            <span>{{ scope_param.row.param }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column prop="test_status" label="测试状态" align="center"></el-table-column>
                <el-table-column prop="use" label="脚本用途" :formatter="useFormat" align="center"></el-table-column>
                <el-table-column label="生效时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_ef_time">
                        <el-tooltip class="item" effect="dark" :content=scope_ef_time.row.ef_time placement="top-start">
                            <span>{{ scope_ef_time.row.ef_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="失效时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_ex_time">
                        <el-tooltip class="item" effect="dark" :content=scope_ex_time.row.ex_time placement="top-start">
                            <span>{{ scope_ex_time.row.ex_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="创建时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_create_time">
                        <el-tooltip class="item" effect="dark" :content=scope_create_time.row.create_time placement="top-start">
                            <span>{{ scope_create_time.row.create_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="更新时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_update_time">
                        <el-tooltip class="item" effect="dark" :content=scope_update_time.row.update_time placement="top-start">
                            <span>{{ scope_update_time.row.update_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="250" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
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
        <el-dialog :title="title" :visible.sync="editVisible" width="65%">
            <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                <el-form-item label="脚本名称" prop="script_name">
                    <el-input v-model="form.script_name"></el-input>
                </el-form-item>
                <el-form-item label="脚本类型" prop="script_type">
                    <el-select v-model="form.script_type" placeholder="请选择脚本类型">
                        <el-option
                                v-for="item in script_type_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="所属分类" prop="category">
                    <el-select v-model="form.category" placeholder="请选择脚本所属分类">
                        <el-option
                                v-for="item in script_category_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="内容" prop="content">
                    <editor
                            v-model="form.content"
                            @init="editorInit"
                            lang="python"
                            theme="tomorrow_night_blue"
                            width="95%"
                            height="500"
                            :options="{
                                enableBasicAutocompletion: true,  // 增加Autocomplete.startCommand命令
                                enableSnippets: true,  // 启用代码块提示功能
                                enableLiveAutocompletion: true,  // 弹出语法提示框
                                tabSize:4,
                                fontSize:20,
                                showPrintMargin: false,   //去除编辑器里的竖线
                                }"></editor>
                </el-form-item>
                <el-form-item label="脚本说明" prop="desc">
                    <el-input type="textarea" v-model="form.desc"></el-input>
                </el-form-item>
                <el-form-item label="脚本参数" prop="param">
                    <el-input v-model="form.param"></el-input>
                </el-form-item>
                <el-form-item label="测试状态" prop="test_status">
                    <el-select v-model="form.test_status" placeholder="请选择脚本测试状态">
                        <el-option
                                v-for="item in test_status_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                        </el-option>
                    </el-select>
<!--                    <el-input v-model="form.test_status"></el-input>-->
                </el-form-item>
                <el-form-item label="脚本用途" prop="use">
                    <el-select v-model="form.use" placeholder="请选择脚本用途">
                        <el-option
                                v-for="item in use_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                    <!--                    <el-input v-model="form.test_status"></el-input>-->
                </el-form-item>
                <el-form-item label="生效时间" prop="ef_time">
                    <el-date-picker
                            v-model="form.ef_time"
                            type="datetime"
                            placeholder="选择日期时间">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="失效时间" prop="ex_time">
                    <el-date-picker
                            v-model="form.ex_time"
                            type="datetime"
                            placeholder="选择日期时间">
                    </el-date-picker>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除脚本 {{script_name}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteScript">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { datetimeFormat } from '../../../util/formatData'
    import Editor from 'vue2-ace-editor'
    export default {
        data() {
            return {
                options: [],
                script_type_options: [
                    {
                        value: '选项1',
                        label: 'Shell脚本'
                    }, {
                        value: '选项2',
                        label: 'Python脚本'
                    }
                ],
                script_category_options: [
                    {
                        value: '选项2',
                        label: '服务器脚本'
                    }
                ],
                test_status_options: [
                    {
                        value: '选项1',
                        label: '已测'
                    }, {
                        value: '选项2',
                        label: '未测'
                    }
                ],
                use_options: [
                    {
                        value: 0,
                        label: '脚本'
                    }, {
                        value: 1,
                        label: '巡检脚本'
                    }
                ],
                script_name: '',
                keywords: '',
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                title: '',
                editVisible: false,
                deleteVisible: false,
                datetimeFormat: null,
                loading: true,
                pageTotal: 0,
                form: {},
                idx: -1,
                id: -1,
                rules: {
                    script_name: [
                        { required: true, message: '请输入脚本名' }
                    ],
                    script_type: [
                        { required: true, message: '请选择脚本类型', trigger: 'change' }
                    ],
                    category: [
                        { required: true, message: '请选择脚本所属分类', trigger: 'change' }
                    ],
                    content: [
                        { required: true, message: '请输入脚本内容', trigger: 'change' }
                    ],
                    test_status: [
                        { required: true, message: '请选择脚本测试状态', trigger: 'change' }
                    ],
                    use: [
                        { required: true, message: '请选择脚本用途', trigger: 'change' }
                    ],
                },
            };

        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getData();
            this.datetimeFormat = datetimeFormat;
        },
        methods: {
            // 格式化脚本用途
            useFormat(row) {
                if(row.use===0) {
                    return '脚本'
                }else if(row.use===1){
                    return '巡检脚本'
                }
            },
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword=this.keywords;
                let url=this.url;
                if(keyword) {
                    url=`automation/api/script/?name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url=`automation/api/script/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }
                this.$http.get(url, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                    this.loading = false;
                }).catch(  (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
                });
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 触发删除按钮
            handleDelete(index, row) {
                this.id = row.id;
                this.form = row;
                this.script_name = row.script_name;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteScript() {
                this.$http.delete(`automation/api/script/${this.id}/`,
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200 || res.status === 204) {
                        this.$message.success('删除成功！');
                        this.deleteVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('删除失败！');
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
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
            handleEdit(index, row) {
                this.id = row.id;
                this.form = row;
                this.title = "编辑";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 新增操作
            handleCreate() {
                this.form = {};
                this.title = "新增";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                if(this.title==="编辑") {this.$http.put(`automation/api/script/${this.id}/`,
                    this.form,
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('修改成功！');
                        this.editVisible = false;
                        this.getData();
                    }else{
                        this.$message.success('修改失败！');
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
                }else {
                    this.$refs.form.validate((valid) => {
                        if (valid) {
                            this.$http.post(`automation/api/script/`,
                                this.form,
                                {
                                    headers:{
                                        'token': this.token
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
                }

            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            editorInit() {
                require("brace/ext/language_tools");
                require("brace/mode/python");
                // require("brace/mode/javascript");
                require("brace/mode/less");
                require("brace/snippets/python");
                require("brace/theme/tomorrow_night_blue");
            },
        },
        components: {
            'editor': Editor,
        }
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
