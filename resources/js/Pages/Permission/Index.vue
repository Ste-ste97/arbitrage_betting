<template>
    <div class="card">

        <Toolbar class="mb-4">
            <template #start>
                <Button v-has-permission="{props: $page.props, permissions: ['permissions.create']}" class="p-button-success mr-2 mb-2" icon="pi pi-plus" label="New Group" @click="createNewGroup()"/>
            </template>

            <template #end>
                <Button class="p-button-help mb-2" icon="pi pi-upload" label="Export" @click="exportCSV($event)"/>
            </template>
        </Toolbar>
        <div class="card">
            <DataTable ref="dt" v-model:expandedRows="expandedRows" :filters="filters"
                       :paginator="true" :rows="10" :rowsPerPageOptions="[10,25,50]"
                       :value="permissions" responsiveLayout="scroll">
                <template #header>
                    <Button class="mb-2 mr-2" icon="pi pi-plus" label="Expand All" @click="expandAll"/>
                    <Button class="mb-2" icon="pi pi-minus" label="Collapse All" @click="collapseAll"/>
                    <div class="table-header flex flex-column md:flex-row md:justiify-content-between">
                        <h5 class="mb-2 md:m-0 p-as-md-center">Manage Permissions</h5>
                        <InputText v-model="filters['global'].value" class="p-inputtext-sm" placeholder="Search..."/>
                    </div>
                </template>
                <template #empty>
                    No permissions found.
                </template>

                <Column :expander="true" headerStyle="width: 3rem"/>

                <Column field="group_name" header="Group Name"></Column>
                <Column field="guard_name" header="Guard Name" sortable></Column>

                <Column :exportable="false">
                    <template #body="slotProps">
                        <Button v-has-permission="{props: $page.props, permissions: ['permissions.edit']}" class="p-button-rounded mr-2" icon="pi pi-pencil" @click="editGroup(slotProps.data)"/>
                        <Button v-has-permission="{props: $page.props, permissions: ['permissions.delete']}" class="p-button-rounded p-button-danger" icon="pi pi-trash" iconPos="left"
                                @click="deleteResource(slotProps.data.id)"/>
                    </template>
                </Column>

                <template #expansion="slotProps">
                    <Button v-has-permission="{props: $page.props, permissions: ['permissions.create']}" class="p-button-success mr-2 mb-2" icon="pi pi-plus" label="New Permission"
                            @click="createNewPermission(slotProps.data)"/>

                    <DataTable :value="slotProps.data.children" class="pt-4" responsiveLayout="scroll">
                        <Column :sortable="true" field="id" header="Id"></Column>
                        <Column :sortable="true" field="type" header="Type"></Column>
                        <Column field="description" header="Description"></Column>
                        <Column :exportable="false">
                            <template #body="slotProps">
                                <Button v-has-permission="{props: $page.props, permissions: ['permissions.edit']}" class="p-button-rounded mr-2" icon="pi pi-pencil"
                                        @click="editPermission(slotProps.data)"/>
                                <Button v-has-permission="{props: $page.props, permissions: ['permissions.delete']}" class="p-button-rounded p-button-danger" icon="pi pi-trash" iconPos="left"
                                        @click="deleteResource(slotProps.data.id)"/>
                            </template>
                        </Column>
                    </DataTable>
                </template>
            </DataTable>
        </div>

        <GroupForm v-model:visible="formGroupVisible" :action="action" :group="group"/>
        <PermissionForm v-model:visible="formPermissionVisible" :action="action" :group="group" :permission="permission"/>
    </div>
</template>

<script>
import AuthenticatedLayout from "@/Layouts/Authenticated.vue";
import GroupForm from "./Partials/GroupForm.vue"
import PermissionForm from "./Partials/PermissionForm.vue"
import {FilterMatchMode} from 'primevue/api';

export default {
    layout     : AuthenticatedLayout,
    components : {
        GroupForm,
        PermissionForm
    },
    props      : {
        permissions : Object,
    },
    data() {
        return {
            group                 : null,
            permission            : null,
            formGroupVisible      : false,
            formPermissionVisible : false,
            action                : "",
            filters               : {},
            expandedRows          : []
        }
    },
    created() {
        this.initFilters();
    },
    methods : {
        exportCSV() {
            this.$refs.dt.exportCSV();
        },
        deleteResource(id) {
            this.$confirm.require({
                message : 'Are you sure you want to delete this group/permission?',
                header  : 'Confirmation',
                icon    : 'pi pi-exclamation-triangle',
                accept  : () => {
                    this.$inertia.delete(route('permissions.destroy', id))
                },
                reject  : () => {
                }
            });
        },
        createNewGroup() {
            this.group            = null
            this.action           = "Create"
            this.formGroupVisible = true;
        },
        editGroup(group) {
            this.group            = group;
            this.action           = "Edit"
            this.formGroupVisible = true;
        },
        createNewPermission(group) {
            this.permission            = null
            this.group                 = group;
            this.action                = "Create"
            this.formPermissionVisible = true;
        },
        editPermission(permission) {
            this.permission            = permission;
            this.action                = "Edit"
            this.formPermissionVisible = true;
        },
        initFilters() {
            this.filters = {
                'global' : {value : null, matchMode : FilterMatchMode.CONTAINS},
            }
        },
        collapseAll() {
            this.expandedRows = [];
        },
        expandAll() {
            this.expandedRows = this.permissions.filter(p => p.id);
        }
    }
};
</script>

<style lang="scss" scoped>
.table-header {
    display         : flex;
    align-items     : center;
    justify-content : space-between;

    @media screen and (max-width : 960px) {
        align-items : start;
    }
}
</style>
