(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2fe0c78d"],{"055d":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"wrapper"},[a("div",{staticClass:"container"},[a("el-input",{staticStyle:{width:"200px","margin-bottom":"15px"},attrs:{type:"text",placeholder:"请输入中间件名称",clearable:""},model:{value:e.keywords,callback:function(t){e.keywords=t},expression:"keywords"}}),a("el-button",{staticClass:"change_el_button",staticStyle:{"margin-left":"10px"},on:{click:e.handleSearch}},[e._v("查询")]),a("el-button",{attrs:{type:"primary",icon:"el-icon-circle-plus-outline"},on:{click:e.handleCreate}},[e._v("新增")]),a("el-table",{staticClass:"user-table",staticStyle:{width:"100%"},attrs:{data:e.tableData,border:"","max-height":"600"}},[a("el-table-column",{attrs:{type:"selection",align:"center"}}),a("el-table-column",{attrs:{type:"index",label:"序号",align:"center"}}),a("el-table-column",{attrs:{prop:"name",label:"中间件名称",align:"center",width:"120"}}),a("el-table-column",{attrs:{prop:"middleware_type",label:"中间件类型",align:"center",width:"120"}}),a("el-table-column",{attrs:{prop:"ip_address",label:"中间件IP",align:"center"}}),a("el-table-column",{attrs:{prop:"port",label:"端口号",align:"center"}}),a("el-table-column",{attrs:{prop:"username",label:"用户名",align:"center"}}),a("el-table-column",{attrs:{prop:"main_mode",label:"维护模式",align:"center"}}),a("af-table-column",{attrs:{prop:"is_monitor",label:"是否监控",align:"center"}}),a("el-table-column",{attrs:{label:"操作",width:"200",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{type:"text",icon:"el-icon-edit"},on:{click:function(a){return e.handleEdit(t.$index,t.row)}}},[e._v("编辑")]),a("el-button",{staticClass:"danger",attrs:{type:"text",icon:"el-icon-delete"},on:{click:function(a){return e.handleDelete(t.$index,t.row)}}},[e._v("删除")])]}}])})],1),a("div",{staticClass:"pagination"},[a("el-pagination",{attrs:{background:"",layout:"total, prev, pager, next","current-page":e.query.pageIndex,"page-size":e.query.pageSize,total:e.pageTotal},on:{"current-change":e.handlePageChange}})],1)],1),a("el-dialog",{attrs:{title:e.title,visible:e.editVisible,width:"30%"},on:{"update:visible":function(t){e.editVisible=t}}},[a("el-form",{ref:"form",attrs:{rules:e.rules,model:e.form,"label-width":"93px"}},[a("el-form-item",{attrs:{label:"中间件名称",prop:"name"}},[a("el-input",{model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),a("el-form-item",{attrs:{label:"中间件类型",prop:"middleware_type"}},[a("el-select",{attrs:{placeholder:"请选择","popper-append-to-body":!1},model:{value:e.form.middleware_type,callback:function(t){e.$set(e.form,"middleware_type",t)},expression:"form.middleware_type"}},e._l(e.options,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",{attrs:{label:"IP地址",prop:"ip_address"}},[a("el-input",{model:{value:e.form.ip_address,callback:function(t){e.$set(e.form,"ip_address",t)},expression:"form.ip_address"}})],1),a("el-form-item",{attrs:{label:"端口号",prop:"port"}},[a("el-input",{model:{value:e.form.port,callback:function(t){e.$set(e.form,"port",t)},expression:"form.port"}})],1),a("el-form-item",{attrs:{label:"用户名",prop:"username"}},[a("el-input",{model:{value:e.form.username,callback:function(t){e.$set(e.form,"username",t)},expression:"form.username"}})],1),a("el-form-item",{attrs:{label:"密码",prop:"password"}},[a("el-input",{attrs:{type:"password"},model:{value:e.form.password,callback:function(t){e.$set(e.form,"password",t)},expression:"form.password"}})],1),a("el-form-item",{attrs:{label:"维护模式",prop:"main_mode"}},[a("el-select",{model:{value:e.form.main_mode,callback:function(t){e.$set(e.form,"main_mode",t)},expression:"form.main_mode"}},e._l(e.options_main_mode,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",{attrs:{label:"是否监控",prop:"is_monitor"}},[a("el-select",{model:{value:e.form.is_monitor,callback:function(t){e.$set(e.form,"is_monitor",t)},expression:"form.is_monitor"}},e._l(e.is_monitor_options,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1)],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{staticClass:"change_el_button",on:{click:function(t){e.editVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:e.saveEdit}},[e._v("确 定")])],1)],1),a("el-dialog",{attrs:{title:"提示",visible:e.deleteVisible,width:"25%"},on:{"update:visible":function(t){e.deleteVisible=t}}},[a("span",[e._v("确定要删除 "+e._s(e.name)+" 中间件信息吗？")]),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{staticClass:"change_el_button",on:{click:function(t){e.deleteVisible=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:e.deleteDB}},[e._v("确 定")])],1)])],1)])},i=[],n=(a("99af"),a("b0c0"),{data:function(){return{options_main_mode:[{value:"否",label:"否"},{value:"是",label:"是"}],is_monitor_options:[{value:"是"},{value:"否"}],options:[{value:"WEBLOGIC",label:"WEBLOGIC"},{value:"REDIS",label:"REDIS"},{value:"TOMCAT",label:"TOMCAT"},{value:"RABBITMQ",label:"RABBITMQ"},{value:"WEBSPHERE",label:"WEBSPHERE"}],keywords:"",title:"",query:{address:"",name:"",pageIndex:1,pageSize:10},tableData:[],multipleSelection:[],delList:[],editVisible:!1,assignVisible:!1,deleteVisible:!1,pageTotal:0,form:{},idx:-1,id:-1,rules:{name:[{required:!0,message:"请输入中间件名称",trigger:"blur"}],ip_address:[{required:!0,message:"请输入中间件地址",trigger:"blur"}]},name:""}},created:function(){this.getData()},methods:{getData:function(){var e=this,t=this.keywords,a=this.url;a=t?"monitor/api/middleware/?name=".concat(t,"&current_page=").concat(this.query.pageIndex,"&pre_page=").concat(this.query.pageSize):"monitor/api/middleware/?current_page=".concat(this.query.pageIndex,"&pre_page=").concat(this.query.pageSize),this.$http.get("".concat(a),{headers:{token:localStorage.getItem("token")}}).then((function(t){e.tableData=t.data.data,e.pageTotal=t.data.total_count})).catch((function(t){e.$message.error(JSON.stringify(t.response.data))}))},handleSearch:function(){this.$set(this.query,"pageIndex",1),this.getData()},handleDelete:function(e,t){this.id=t.id,this.form=t,this.name=t.name,this.deleteVisible=!0},deleteDB:function(){var e=this;this.$http.put("monitor/api/middleware/delete/",{ids:[this.id]},{headers:{token:localStorage.getItem("token")}}).then((function(t){200===t.status?(e.$message.success("删除成功！"),e.deleteVisible=!1,e.getData()):e.$message.error("删除失败！")})).catch((function(t){e.$message.error(JSON.stringify(t.response.data))}))},handleSelectionChange:function(e){this.multipleSelection=e},delAllSelection:function(){var e=this.multipleSelection.length,t="";this.delList=this.delList.concat(this.multipleSelection);for(var a=0;a<e;a++)t+=this.multipleSelection[a].name+" ";this.$message.error("删除了".concat(t)),this.multipleSelection=[]},handleEdit:function(e,t){var a=this;this.id=t.id,this.form=t,this.title="编辑",this.editVisible=!0,this.$nextTick((function(){a.$refs.form.clearValidate()}))},handleCreate:function(){var e=this;this.title="新增",this.editVisible=!0,this.createVisible=!1,this.form={},this.$nextTick((function(){e.$refs.form.clearValidate()}))},saveEdit:function(){var e=this;"编辑"===this.title?this.$refs.form.validate((function(t){if(!t)return e.$message.warning("参数错误"),!1;e.$http.put("monitor/api/middleware/".concat(e.id,"/"),e.form,{headers:{token:localStorage.getItem("token")}}).then((function(t){200===t.status?(e.$message.success("修改成功！"),e.editVisible=!1,e.getData()):e.$message.error("修改失败！")})).catch((function(t){e.$message.error(JSON.stringify(t.response.data))}))})):this.$refs.form.validate((function(t){if(!t)return e.$message.warning("参数错误"),!1;e.$http.post("monitor/api/middleware/",e.form,{headers:{token:localStorage.getItem("token")}}).then((function(t){200===t.status||201===t.status?(e.$message.success("创建成功！"),e.editVisible=!1,e.getData()):e.$message.error("创建失败！")})).catch((function(t){e.$message.error(JSON.stringify(t.response.data))}))}))},handlePageChange:function(e){this.$set(this.query,"pageIndex",e),this.getData()}}}),o=n,r=(a("f462"),a("2877")),s=Object(r["a"])(o,l,i,!1,null,"b737ea2e",null);t["default"]=s.exports},ecbf:function(e,t,a){},f462:function(e,t,a){"use strict";var l=a("ecbf"),i=a.n(l);i.a}}]);