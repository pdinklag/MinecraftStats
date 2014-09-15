<?
    define('NBT_END', 0);
    define('NBT_BYTE', 1);
    define('NBT_SHORT', 2);
    define('NBT_INT', 3);
    define('NBT_LONG', 4);
    define('NBT_FLOAT', 5);
    define('NBT_DOUBLE', 6);
    define('NBT_BYTE_ARRAY', 7);
    define('NBT_STRING', 8);
    define('NBT_LIST', 9);
    define('NBT_COMPOUND', 10);
    define('NBT_INT_ARRAY', 11);
    
    function nbt_readTag($f) {
        return unpack('C', fread($f, 1))[1];
    }
    
    function nbt_readString($f) {
        $len = unpack('n', fread($f, 2))[1];
        if($len > 0) {
            return utf8_decode(fread($f, $len));
        } else {
            return '';
        }
    }
    
    function nbt_readCompound($f) {
        $compound = [];
        
        $next = nbt_readTag($f);
        while($next != NBT_END) {
            $name = nbt_readString($f);
            $compound[$name] = nbt_readDynamic($f, $next);
            
            $next = nbt_readTag($f);
        }
        
        return $compound;
    }
    
    function nbt_readList($f) {
        $list = [];
        $tag = nbt_readTag($f);
        $len = unpack('N', fread($f, 4))[1];
        
        for($i = 0; $i < $len; $i++) {
            $list[$i] = nbt_readDynamic($f, $tag);
        }
        
        return $list;
    }
    
    function signedInt16($s) {
        if($s >= 0x8000) {
            return -1 - ($s & 0x7FFF);
        } else {
            return $s;
        }
    }
    
    function signedInt32($i) {
        if($i >= 0x80000000) {
            return -1 - ($i & 0x7FFFFFFF);
        } else {
            return $i;
        }
    }
    
    function signedInt64($l) {
        if($l >= 0x8000000000000000) {
            return -1 - ($l & 0x7FFFFFFFFFFFFFFF);
        } else {
            return $l;
        }
    }
    
    function nbt_readDynamic($f, $tag) {
        switch($tag) {
            case NBT_BYTE:
                return unpack('c', fread($f, 1))[1];

            case NBT_SHORT:
                return signedInt16(unpack('n', fread($f, 2))[1]);

            case NBT_INT:
                return signedInt32(unpack('N', fread($f, 4))[1]);
                
            case NBT_LONG:
                $l = (unpack('N', fread($f, 4))[1] * 0x100000000) + (int)unpack('N', fread($f, 4))[1];
                return signedInt64($l);
                
            case NBT_FLOAT:
                return unpack('f', strrev(fread($f, 4)))[1];
                
            case NBT_DOUBLE:
                return unpack('d', strrev(fread($f, 8)))[1];
                
            case NBT_BYTE_ARRAY:
                $len = unpack('N', fread($f, 4))[1];
                fread($f, $len); //discard
                return '(BYTE_ARRAY)';
                
            case NBT_STRING:
                return nbt_readString($f);
            
            case NBT_LIST:
                return nbt_readList($f);
                
            case NBT_COMPOUND:
                return nbt_readCompound($f);
                
            case NBT_INT_ARRAY:
                $len = unpack('N', fread($f, 4))[1];
                fread($f, 4 * $len); //discard
                return '(INT_ARRAY)';
        }
    }

    /* NBT reader */
    function nbtdecode($nbt) {
        $f = fopen('php://memory', 'r+');
        fwrite($f, $nbt);
        rewind($f);
        
        $result = FALSE;
        
        $tag = nbt_readTag($f);
        if($tag == NBT_COMPOUND) {
            nbt_readString($f); //discard name
            $result = nbt_readCompound($f);
        } else {
            die('top level needs to be a compound');
        }
        
        fclose($f);
        return $result;
    }
?>
