import numpy as np
from lxml import etree
import shutil, os
import subprocess

np.random.seed(2)
voxSize = 0.01
r = np.random.random([1,300,300])
r1 = np.random.random([1,300,300])
voxels = np.zeros_like(r, dtype=int)
voxels[r>0.99] = 2
control = r1 * 2 - 1
control[voxels==0] = 0

def write_VXD(body, phaseoffset, exp_id, exp_name):
    z,y,x = body.shape
    body_flatten = body.reshape(1,-1)
    phaseoffset_flatten = phaseoffset.reshape(1,-1)
    # generate VXD
    child = etree.SubElement
    root = etree.Element("VXD")
    RawPrint = child(root, "RawPrint")
    RawPrint.set('replace', 'VXA.RawPrint')
    RawPrint.text = ""
    # Enable Attachment
    AttachDetach = child(root, "AttachDetach")
    AttachDetach.set('replace', 'VXA.Simulator.AttachDetach')
    child(AttachDetach, 'EnableCollision').text = '1'
    child(AttachDetach, 'EnableAttach').text = '1'
    child(AttachDetach, 'watchDistance').text = '1'
    child(AttachDetach, 'SafetyGuard').text = '3000'
    # Attach Condition (attach only happens when this value > 0)
    AttachCondition = child(AttachDetach, 'AttachCondition')
    if exp_name=="attach_all":
        formula_attach = "<Condition_0><mtCONST>1</mtCONST></Condition_0>"
        AttachCondition.append(etree.fromstring(formula_attach))
    elif exp_name=="attach_area_circle":
        # attach = r^2 - (x-50)^2 + (y-50)^2
        r = 10
        formula_attach = """
                        <Condition_0>
                        <mtSUB>
                            <mtCONST>{}</mtCONST>
                            <mtADD>
                                <mtMUL>
                                    <mtSUB>
                                        <mtVAR>x</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                    </mtSUB>
                                    <mtSUB>
                                        <mtVAR>x</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                    </mtSUB>
                                </mtMUL>
                                <mtMUL>
                                    <mtSUB>
                                        <mtVAR>y</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                    </mtSUB>
                                    <mtSUB>
                                        <mtVAR>y</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                    </mtSUB>
                                </mtMUL>
                            </mtADD>
                        </mtSUB>
                        </Condition_0>
        """.format(r*r*voxSize*voxSize, x/2*voxSize, x/2*voxSize, y/2*voxSize, y/2*voxSize)
        AttachCondition.append(etree.fromstring(formula_attach))
        RawPrint.text += "{{{setting}}}"+f"<cylinder><x>{x/2*voxSize}</x><y>{y/2*voxSize}</y><r>{r*voxSize}</r></cylinder>"
    elif exp_name=="attach_area_rect":
        a = 50 ; b = 5
        formula_attach = """
                        <Condition_0>
                        <mtSUB>
                            <mtCONST>{}</mtCONST>
                            <mtABS>
                                <mtSUB>
                                    <mtVAR>x</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                </mtSUB>
                            </mtABS>
                        </mtSUB>
                        </Condition_0>
                        """.format(a*voxSize, x/2*voxSize)
        AttachCondition.append(etree.fromstring(formula_attach))
        formula_attach = """
                        <Condition_1>
                        <mtSUB>
                            <mtCONST>{}</mtCONST>
                            <mtABS>
                                <mtSUB>
                                    <mtVAR>y</mtVAR>
                                        <mtCONST>{}</mtCONST>
                                </mtSUB>
                            </mtABS>
                        </mtSUB>
                        </Condition_1>
                        """.format(b*voxSize, y/2*voxSize)
        AttachCondition.append(etree.fromstring(formula_attach))
        RawPrint.text += "{{{setting}}}"+f"<rectangle><x>{x/2*voxSize}</x><y>{y/2*voxSize}</y><a>{a*voxSize}</a><b>{b*voxSize}</b></rectangle>"

    elif exp_name=="attach_time":
        t = 3
        formula_attach = """
                        <Condition_0>
                        <mtSUB>
                            <mtVAR>t</mtVAR>
                            <mtCONST>{}</mtCONST>
                        </mtSUB>
                        </Condition_0>
                        """.format(t)
        AttachCondition.append(etree.fromstring(formula_attach))
        RawPrint.text += "{{{setting}}}"+f"<flash><t>{t}</t></flash>"
    else:
        print("ERROR: exp_name unexpected.")

    # Stop Condition 10 sec
    StopCondition = child(root, "StopCondition")
    StopCondition.set('replace', 'VXA.Simulator.StopCondition')
    StopConditionFormula = child(StopCondition, "StopConditionFormula")
    # stop happen at (t - 10 > 0)
    stop_condition_formula = """
    <mtSUB>
        <mtVAR>t</mtVAR>
        <mtCONST>10</mtCONST>
    </mtSUB>
    """
    StopConditionFormula.append(etree.fromstring(stop_condition_formula))
    # Record History
    RecordHistory = child(root, "RecordHistory")
    RecordHistory.set('replace', 'VXA.Simulator.RecordHistory')
    child(RecordHistory, "RecordStepSize").text = '100'
    child(RecordHistory, "RecordVoxel").text = '1'
    child(RecordHistory, "RecordLink").text = '0'
    # Gravity
    GravAcc = child(root, "GravAcc")
    GravAcc.set('replace', 'VXA.Environment.Gravity.GravAcc')
    GravAcc.text = '-9.8' # instead of -9.8

    # ForceField
    ForceField = child(root, "ForceField")
    ForceField.set('replace', "VXA.Simulator.ForceField")
    # x_f = 100*y + (-100)*atan(x-50);
    x_forcefield = child(ForceField, "x_forcefield")
    formula_x = """
    <mtADD>
        <mtMUL>
            <mtCONST>100</mtCONST>
            <mtSUB>
                <mtVAR>y</mtVAR>
                <mtCONST>{}</mtCONST>
            </mtSUB>
        </mtMUL>
        <mtMUL>
            <mtCONST>-100</mtCONST>
            <mtATAN>
                <mtSUB>
                    <mtVAR>x</mtVAR>
                    <mtCONST>{}</mtCONST>
                </mtSUB>
            </mtATAN>
        </mtMUL>
    </mtADD>
    """.format(y/2*voxSize, x/2*voxSize)
    x_forcefield.append(etree.fromstring(formula_x))
    # y_f = -100*x + (-100)*atan(y-50);
    y_forcefield = child(ForceField, "y_forcefield")
    formula_y = """
    <mtADD>
        <mtMUL>
            <mtCONST>-100</mtCONST>
            <mtSUB>
                <mtVAR>x</mtVAR>
                <mtCONST>{}</mtCONST>
            </mtSUB>
        </mtMUL>
        <mtMUL>
            <mtCONST>-100</mtCONST>
            <mtATAN>
                <mtSUB>
                    <mtVAR>y</mtVAR>
                    <mtCONST>{}</mtCONST>
                </mtSUB>
            </mtATAN>
        </mtMUL>
    </mtADD>
    """.format(x/2*voxSize, y/2*voxSize)
    y_forcefield.append(etree.fromstring(formula_y))

    # Main Structure and PhaseOffset
    Structure = child(root, "Structure")
    Structure.set('replace', 'VXA.VXC.Structure')
    Structure.set('Compression', 'ASCII_READABLE')
    child(Structure, "X_Voxels").text = str(x)
    child(Structure, "Y_Voxels").text = str(y)
    child(Structure, "Z_Voxels").text = str(z)
    data = child(Structure, "Data")
    for i in range(body_flatten.shape[0]):
        layer = child(data, "Layer")
        str_layer = "".join([str(c) for c in body_flatten[i]])
        layer.text = etree.CDATA(str_layer)
    phaseoffset = child(Structure, "PhaseOffset")
    for i in range(phaseoffset_flatten.shape[0]):
        layer = child(phaseoffset, "Layer")
        str_layer = ",".join([str(c) for c in phaseoffset_flatten[i]])
        layer.text = etree.CDATA(str_layer)
    with open(f"{exp_name}/exp.vxd", 'wb') as file:
        file.write(etree.tostring(root))


# Start Experiments
exp_names = ["attach_all", "attach_area_circle", "attach_area_rect", "attach_time"]
for exp_id, exp_name in enumerate(exp_names):
    try:
        os.mkdir(exp_name)
    except:
        pass
    try:
        shutil.copyfile("./base.vxa", f"{exp_name}/base.vxa")
    except:
        print("base.vxa not found.")

    write_VXD(voxels, control, exp_id, exp_name)