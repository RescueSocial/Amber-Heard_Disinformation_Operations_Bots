 <?php
    defined('BASEPATH') OR exit('No direct script access allowed');
?>
<?php $this->load->view('elements/header', $title); ?>
<!-- page content -->
    <div class="right_col" role="main">
        <br><br><br>
        <!--Display Any Error or Success Message-->
        <?php 
            if($this->session->flashdata('success')){
                $msg['msg'] = $this->session->flashdata('success');
                $this->load->view('flash_messages/success', $msg);
            }else if($this->session->flashdata('error')){
                $msg['msg'] = $this->session->flashdata('error');
                $this->load->view('flash_messages/error', $msg);
            } 
        ?>
        <div id="page-content">
            <!-- Dashboard 2 Header -->
            <!-- <div class="content-header">
               <h2>Upload file (pdf, jpg, png)</h2>
            </div>
            <form name="" action="preprocessor/uploadfile" method="post" enctype="multipart/form-data"><br />
                <h3>Select file to upload for Pre-Processing:</h3>
                <br />
                <input type="file" name="fileToUpload" id="fileToUpload">
                <br />
                <input type="submit" value="Upload">
            </form> -->
            <?php
                echo form_open_multipart('preprocessor/uploadfile', array('name' => 'addemployee', 'class'=>'form-horizontal'));
            ?>
                <div class="form-group">
                    <br />
                    <h3>Select file to upload for Pre-Processing:</h3>
                    <br />
                    <!-- <label class="control-label col-sm-4">Select file to upload for Pre-Processing:</label> -->
                    <div class="col-sm-10">
                        <input type="file" class=" pull-center" id="fileToUpload" name="fileToUpload">
                    </div>
                </div>
                
                <div class="form-group">
                    <div class="col-sm-10">
                        <input type="submit" class="btn btn-primary pull-center" name="save" value="Pre-Process" /> 
                    </div>
                </div>
                <br />
                <?php if (isset($result) && $result != '') : ?>
                    <div class="col-8">
                    <label class="control-label col-8"><?php echo($fileName);?></label>
                    </div>
                    <div class="col-8">
                        <textarea class="form-control" rows="30" cols="100" id="post_body" name="post_body"><?php echo($result);?></textarea>
                    </div>
                <?php endif; ?>
                <?php if (isset($downloadfname) && $downloadfname != '') : ?>
                    <a href="<?php echo base_url(); ?>public/assets/preprocessorFiles/output/<?php echo $downloadfname; ?>">Download Result</a>
                <?php endif; ?>
            <?php
                echo form_close();
            ?>
        </div>
    </div>
<?php $this->load->view('elements/footer'); ?>
		